const express = require('express');
const path = require('path');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, '.')));

// LiveKit configuration
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL || 'wss://liquid-milk-balls-web-production.up.railway.app';

// Token generation for Mirror's Echo room
app.post('/api/token', async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
    return res.status(500).json({
      error: 'LiveKit not configured. Set LIVEKIT_API_KEY and LIVEKIT_API_SECRET environment variables.'
    });
  }

  try {
    const { roomName, identity } = req.body;

    if (!roomName || !identity) {
      return res.status(400).json({ error: 'Missing roomName or identity' });
    }

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: '2h',
    });

    // For main display: can subscribe only
    // For remote participants: can publish and subscribe
    const canPublish = identity !== 'main-display';

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
    console.error('Error generating token:', error);
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

// OBS WHIP endpoint for streaming processed video to Mirror's Echo
app.get('/api/obs-whip-token', async (req, res) => {
  if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
    return res.status(500).json({
      error: 'LiveKit not configured'
    });
  }

  try {
    const roomName = req.query.room || 'mirrors-echo-main';
    const identity = req.query.identity || 'obs-processed-video';

    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: identity,
      ttl: '24h', // Long TTL for OBS
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
    console.error('Error generating OBS WHIP token:', error);
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'mirrors-echo-main.html'));
});

app.get('/join', (req, res) => {
  res.sendFile(path.join(__dirname, 'mirrors-echo-remote.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✨ Mirror's Echo server running on port ${PORT}`);
  console.log(`📺 Main display: http://localhost:${PORT}/`);
  console.log(`📹 Remote join: http://localhost:${PORT}/join`);
  
  if (LIVEKIT_API_KEY && LIVEKIT_API_SECRET) {
    console.log(`\n🎥 LiveKit configured: ${LIVEKIT_URL}`);
    console.log(`📊 API Endpoints:`);
    console.log(`   POST /api/token - Generate room tokens`);
    console.log(`   GET /api/obs-whip-token - Get OBS WHIP streaming URL`);
  } else {
    console.log(`\n⚠️  LiveKit not configured. Set LIVEKIT_API_KEY and LIVEKIT_API_SECRET`);
  }
});
