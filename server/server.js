const express = require("express");
const path = require("path");
const http = require("http");
const { WebSocketServer } = require("ws");
const { AccessToken, RoomServiceClient } = require("livekit-server-sdk");
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
app.use(express.static(path.join(__dirname, '..')));

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

// Mirror's Echo endpoints

// Token generation for Mirror's Echo room (supports both main display and remote participants)
app.post("/api/token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
    return res.status(500).json({
      error: "LiveKit not configured. Set LIVEKIT_API_KEY and LIVEKIT_API_SECRET environment variables."
    });
  }

  try {
    const { roomName, identity } = req.body;

    if (!roomName || !identity) {
      return res.status(400).json({ error: "Missing roomName or identity" });
    }

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: "2h",
    });

    // For main display: can subscribe only
    // For remote participants: can publish and subscribe
    const canPublish = identity !== "main-display";

    token.addGrant({
      room: roomName,
      roomJoin: true,
      canPublish: canPublish,
      canSubscribe: true,
    });

    res.json({
      token: await token.toJwt(),
      url: LIVEKIT_URL
    });
  } catch (error) {
    console.error("Error generating Mirror's Echo token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

// OBS WHIP endpoint for streaming processed video to Mirror's Echo
app.get("/api/obs-whip-token", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const roomName = req.query.room || "mirrors-echo-main";
    const identity = req.query.identity || "obs-processed-video";

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: "24h", // Long TTL for OBS
    });

    token.addGrant({
      room: roomName,
      roomJoin: true,
      canPublish: true,
      canSubscribe: false,
    });

    const jwt = await token.toJwt();
    const whipUrl = `${LIVEKIT_URL.replace('wss://', 'https://').replace('ws://', 'http://')}/whip?access_token=${jwt}`;

    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      room: roomName,
      whipUrl: whipUrl,
      identity: identity
    });
  } catch (error) {
    console.error("Error generating OBS WHIP token:", error);
    res.status(500).json({ error: "Failed to generate token" });
  }
});

// RTMP Ingress Endpoints (for OBS streaming)

// Create RTMP Ingress for OBS
app.post("/api/create-rtmp-ingress", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const livekitHost = LIVEKIT_URL.replace('wss://', 'https://').replace('ws://', 'http://');
    
    const roomService = new RoomServiceClient(
      livekitHost,
      LIVEKIT_API_KEY,
      LIVEKIT_API_SECRET
    );

    // Create RTMP ingress for processed-output room
    const ingressInfo = await roomService.createIngress({
      inputType: 0, // RTMP_INPUT
      name: 'OBS-RTMP-Stream',
      roomName: PROCESSED_ROOM,
      participantIdentity: 'obs-rtmp-publisher',
      participantName: 'OBS Stream'
    });

    console.log('[RTMP] Ingress created:', ingressInfo.ingressId);

    // Return the RTMP URL and stream key
    res.json({
      success: true,
      ingressId: ingressInfo.ingressId,
      rtmpUrl: ingressInfo.url,
      streamKey: ingressInfo.streamKey,
      fullRtmpUrl: `${ingressInfo.url}/${ingressInfo.streamKey}`,
      room: PROCESSED_ROOM
    });

  } catch (error) {
    console.error('Error creating RTMP ingress:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// List existing RTMP ingresses
app.get("/api/list-ingresses", async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
    return res.status(500).json({
      error: "LiveKit not configured"
    });
  }

  try {
    const livekitHost = LIVEKIT_URL.replace('wss://', 'https://').replace('ws://', 'http://');
    
    const roomService = new RoomServiceClient(
      livekitHost,
      LIVEKIT_API_KEY,
      LIVEKIT_API_SECRET
    );

    const ingresses = await roomService.listIngress({ 
      roomName: PROCESSED_ROOM 
    });

    res.json({
      success: true,
      ingresses: ingresses.map(ing => ({
        id: ing.ingressId,
        name: ing.name,
        url: ing.url,
        streamKey: ing.streamKey,
        room: ing.roomName,
        state: ing.state
      }))
    });

  } catch (error) {
    console.error('Error listing ingresses:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Stripe Payment Endpoints

// Get Stripe publishable key
app.get("/api/stripe-config", (req, res) => {
  const publishableKey = process.env.STRIPE_PUBLISHABLE_KEY;

  if (!publishableKey) {
    return res.status(500).json({
      error: "Stripe not configured"
    });
  }

  res.json({
    publishableKey: publishableKey
  });
});

// Create Stripe Checkout session for Exhibition License
app.post("/api/create-checkout-session", async (req, res) => {
  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;

  if (!STRIPE_SECRET_KEY) {
    return res.status(500).json({
      error: "Payment system not configured. Contact artist for licensing."
    });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: "usd",
            product_data: {
              name: "Exhibition License — The Mirror's Echo",
              description: "Commercial exhibition rights with unlimited sustained experience (no temporal markers)",
            },
            unit_amount: 40000, // $400.00 in cents
          },
          quantity: 1,
        },
      ],
      mode: "payment",
      success_url: `${req.headers.origin}/payment-success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.origin}/payment-cancel.html`,
      metadata: {
        license_type: "exhibition",
      },
    });

    res.json({ sessionId: session.id });
  } catch (error) {
    console.error("Error creating checkout session:", error);
    res.status(500).json({ error: "Failed to create checkout session" });
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
