const express = require("express");
const path = require("path");
const http = require("http");
const { WebSocketServer } = require("ws");
const { AccessToken } = require("livekit-server-sdk");
const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);
const paypal = require("@paypal/checkout-server-sdk");

const PORT = process.env.PORT || 3000;
const app = express();

// LiveKit configuration
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const INPUT_ROOM = process.env.LIVEKIT_ROOM_NAME || "claymation-live";
const PROCESSED_ROOM = process.env.LIVEKIT_PROCESSED_ROOM || "processed-output";

app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.get("/healthz", (_req, res) => res.status(200).send("ok"));

// LiveKit Token Generation Endpoints

// Token for remote camera to publish to input room
app.get("/api/publisher-token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured. Set LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL environment variables."
    });
  }

  try {
    const participantName = req.query.identity || `publisher-${Date.now()}`;

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantName,
      ttl: "2h",
    });

    token.addGrant({
      room: INPUT_ROOM,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
    });

    res.json({
      token: await token.toJwt(),
      url: LIVEKIT_URL,
      room: INPUT_ROOM,
    });
  } catch (error) {
    console.error("Error generating publisher token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

// Token for viewing input room (for OBS Browser Source)
app.get("/api/viewer-token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const participantName = req.query.identity || `viewer-${Date.now()}`;

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantName,
      ttl: "2h",
    });

    token.addGrant({
      room: INPUT_ROOM,
      roomJoin: true,
      canPublish: false,
      canSubscribe: true,
    });

    res.json({
      token: await token.toJwt(),
      url: LIVEKIT_URL,
      room: INPUT_ROOM,
    });
  } catch (error) {
    console.error("Error generating viewer token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

// Token for OBS WHIP to publish processed video
app.get("/api/processed-publisher-token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const participantName = req.query.identity || "obs-processed-output";

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantName,
      ttl: "24h", // Longer TTL for OBS
    });

    token.addGrant({
      room: PROCESSED_ROOM,
      roomJoin: true,
      canPublish: true,
      canSubscribe: false,
    });

    const jwt = await token.toJwt();

    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      room: PROCESSED_ROOM,
      whipUrl: `${LIVEKIT_URL.replace('wss://', 'https://').replace('ws://', 'http://')}/whip?access_token=${jwt}`,
    });
  } catch (error) {
    console.error("Error generating processed publisher token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

// Token for remote users to view processed video
app.get("/api/processed-viewer-token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const participantName = req.query.identity || `processed-viewer-${Date.now()}`;

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantName,
      ttl: "2h",
    });

    token.addGrant({
      room: PROCESSED_ROOM,
      roomJoin: true,
      canPublish: false,
      canSubscribe: true,
    });

    res.json({
      token: await token.toJwt(),
      url: LIVEKIT_URL,
      room: PROCESSED_ROOM,
    });
  } catch (error) {
    console.error("Error generating processed viewer token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: "/ws" });

// Track rooms: { roomName: Set<WebSocket> }
const rooms = new Map();

wss.on("connection", (ws) => {
  console.log("[ws] Client connected");
  ws.currentRoom = null;
  
  const keepalive = setInterval(() => { 
    try { 
      ws.ping(); 
    } catch (e) {
      console.error("[ws] Ping error:", e);
    }
  }, 25000);
  
  ws.on("message", (msg) => {
    try {
      const data = JSON.parse(msg);
      
      // Handle room join
      if (data.type === 'join-room') {
        const roomName = data.room;
        
        // Leave old room if exists
        if (ws.currentRoom && rooms.has(ws.currentRoom)) {
          rooms.get(ws.currentRoom).delete(ws);
          console.log(`[ws] Client left room: ${ws.currentRoom}`);
        }
        
        // Join new room
        if (!rooms.has(roomName)) {
          rooms.set(roomName, new Set());
        }
        rooms.get(roomName).add(ws);
        ws.currentRoom = roomName;
        console.log(`[ws] Client joined room: ${roomName} (${rooms.get(roomName).size} clients)`);
        
        return;
      }
      
      // Broadcast to room or everyone
      const targetRoom = ws.currentRoom;
      const clients = targetRoom && rooms.has(targetRoom) 
        ? rooms.get(targetRoom) 
        : wss.clients;
      
      for (const client of clients) {
        if (client !== ws && client.readyState === client.OPEN) {
          try { 
            client.send(msg); 
          } catch (e) {
            console.error("[ws] Send error:", e);
          }
        }
      }
    } catch (e) {
      console.error("[ws] Message parsing error:", e);
    }
  });
  
  ws.on("close", () => {
    console.log("[ws] Client disconnected");
    
    // Remove from room
    if (ws.currentRoom && rooms.has(ws.currentRoom)) {
      rooms.get(ws.currentRoom).delete(ws);
      console.log(`[ws] Client removed from room: ${ws.currentRoom}`);
      
      // Clean up empty rooms
      if (rooms.get(ws.currentRoom).size === 0) {
        rooms.delete(ws.currentRoom);
        console.log(`[ws] Room deleted: ${ws.currentRoom}`);
      }
    }
    
    clearInterval(keepalive);
  });
  
  ws.on("error", (error) => {
    console.error("[ws] WebSocket error:", error);
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`📺 Main page: http://localhost:${PORT}/`);
  console.log(`📹 Publisher (remote camera): http://localhost:${PORT}/publisher.html`);
  console.log(`👁️  Return viewer (processed video): http://localhost:${PORT}/return-viewer.html`);
  console.log(`🔌 WebSocket: ws://localhost:${PORT}/ws`);

  if (LIVEKIT_API_KEY && LIVEKIT_API_SECRET && LIVEKIT_URL) {
    console.log(`\n🎥 LiveKit configured:`);
    console.log(`   Input room: ${INPUT_ROOM}`);
    console.log(`   Processed room: ${PROCESSED_ROOM}`);
    console.log(`   Server: ${LIVEKIT_URL}`);
    console.log(`\n📊 API Endpoints:`);
    console.log(`   /api/publisher-token - Remote camera publishing`);
    console.log(`   /api/viewer-token - View input (for OBS)`);
    console.log(`   /api/processed-publisher-token - OBS WHIP publishing`);
    console.log(`   /api/processed-viewer-token - View processed output`);
  } else {
    console.log(`\n⚠️  LiveKit not configured. Set these environment variables:`);
    console.log(`   LIVEKIT_API_KEY`);
    console.log(`   LIVEKIT_API_SECRET`);
    console.log(`   LIVEKIT_URL`);
  }
});
