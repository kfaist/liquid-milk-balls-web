const express = require("express");
const path = require("path");
const http = require("http");
const { WebSocketServer } = require("ws");
const { AccessToken } = require('livekit-server-sdk');

const PORT = process.env.PORT || 3000;
const app = express();

// LiveKit configuration
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;

app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.get("/healthz", (_req, res) => res.status(200).send("ok"));

// LiveKit token endpoints
app.get("/api/publisher-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({ error: 'LiveKit not configured' });
    }
    
    const participantIdentity = `publisher-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '2h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'claymation-live',
      canPublish: true,
      canSubscribe: true,
    });
    
    const jwt = await token.toJwt();
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'claymation-live',
      identity: participantIdentity
    });
  } catch (error) {
    console.error('[token] Error:', error);
    res.status(500).json({ error: 'Token generation failed' });
  }
});

app.get("/api/viewer-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({ error: 'LiveKit not configured' });
    }
    
    const participantIdentity = `viewer-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '2h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'claymation-live',
      canPublish: false,
      canSubscribe: true,
    });
    
    const jwt = await token.toJwt();
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'claymation-live',
      identity: participantIdentity
    });
  } catch (error) {
    console.error('[token] Error:', error);
    res.status(500).json({ error: 'Token generation failed' });
  }
});

app.get("/api/processed-publisher-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({ error: 'LiveKit not configured' });
    }
    
    const participantIdentity = `obs-publisher-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '24h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'processed-output',
      canPublish: true,
      canSubscribe: false,
    });
    
    const jwt = await token.toJwt();
    const whipUrl = `${LIVEKIT_URL.replace('wss://', 'https://')}/whip?access_token=${jwt}`;
    
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'processed-output',
      identity: participantIdentity,
      whip_url: whipUrl
    });
  } catch (error) {
    console.error('[token] Error:', error);
    res.status(500).json({ error: 'Token generation failed' });
  }
});

app.get("/api/processed-viewer-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({ error: 'LiveKit not configured' });
    }
    
    const participantIdentity = `output-viewer-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '2h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'processed-output',
      canPublish: false,
      canSubscribe: true,
    });
    
    const jwt = await token.toJwt();
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'processed-output',
      identity: participantIdentity
    });
  } catch (error) {
    console.error('[token] Error:', error);
    res.status(500).json({ error: 'Token generation failed' });
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
  console.log(`🎨 Publisher: http://localhost:${PORT}/td-publisher.html`);
  console.log(`👤 Remote participant: http://localhost:${PORT}/remote-participant.html`);
  console.log(`🎬 Studio control: http://localhost:${PORT}/krista-studio.html`);
  console.log(`🔌 WebSocket: ws://localhost:${PORT}/ws`);
});
