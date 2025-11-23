// LiveKit Token Endpoint - Reads from .env file
require('dotenv').config();
const express = require('express');
const { AccessToken } = require('livekit-server-sdk');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

const API_KEY = process.env.LIVEKIT_API_KEY;
const API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const ROOM = process.env.LIVEKIT_ROOM_NAME || 'mirror-echo';

if (!API_KEY || !API_SECRET) {
  console.error('ERROR: LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in .env file');
  process.exit(1);
}

app.use(cors());
app.use(express.json());

// Token generation endpoint
app.get('/token', (req, res) => {
  try {
    const { identity, roomName } = req.query;
    const room = roomName || ROOM;
    
    if (!identity) {
      return res.status(400).json({ 
        error: 'Missing identity parameter' 
      });
    }
    
    console.log(`Generating token for ${identity} in room ${room}`);
    
    // Create access token
    const at = new AccessToken(API_KEY, API_SECRET, {
      identity: identity,
      ttl: '6h',
    });
    
    // Grant permissions
    at.addGrant({
      roomJoin: true,
      room: room,
      canPublish: true,
      canPublishData: true,
      canSubscribe: true,
    });
    
    const token = at.toJwt();
    
    res.json({
      token,
      url: LIVEKIT_URL,
      room: room,
      identity: identity,
      expiresIn: '6h',
      timestamp: new Date().toISOString()
    });
    
    console.log(`✓ Token generated for ${identity}`);
    
  } catch (error) {
    console.error('Token generation error:', error);
    res.status(500).json({ 
      error: 'Failed to generate token',
      message: error.message 
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok',
    livekitConfigured: !!(API_KEY && API_SECRET),
    livekitUrl: LIVEKIT_URL,
    room: ROOM,
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log(`🔐 LiveKit Token Endpoint Running`);
  console.log(`   Port: ${PORT}`);
  console.log(`   URL: http://localhost:${PORT}`);
  console.log(`   LiveKit: ${LIVEKIT_URL}`);
  console.log(`   Room: ${ROOM}`);
  console.log('='.repeat(60));
  console.log('\nConfiguration:');
  console.log(`   API Key: ${API_KEY ? '✓ Set' : '✗ Missing'}`);
  console.log(`   API Secret: ${API_SECRET ? '✓ Set' : '✗ Missing'}`);
  console.log('='.repeat(60));
  console.log('\nTest with:');
  console.log(`   curl "http://localhost:${PORT}/token?identity=test&roomName=${ROOM}"`);
  console.log('='.repeat(60));
});
