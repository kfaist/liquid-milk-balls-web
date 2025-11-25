const express = require('express');
const path = require('path');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const PORT = process.env.PORT || 3000;

const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';

// Serve static files
app.use(express.static(__dirname));

// Generate LiveKit token
app.get('/token', (req, res) => {
    const roomName = req.query.room || 'claymation-live';
    const identity = req.query.identity || 'publisher-' + Math.random().toString(36).substr(2, 6);
    const isPublisher = req.query.publisher === 'true';
    
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
            identity: identity,
            ttl: '6h'
        });
        
        token.addGrant({
            room: roomName,
            roomJoin: true,
            canPublish: isPublisher,
            canSubscribe: !isPublisher
        });
        
        const jwt = token.toJwt();
        
        res.json({ 
            token: jwt,
            url: 'wss://claymation-transcription-l6e51sws.livekit.cloud',
            room: roomName,
            identity: identity
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Main route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'mirrors-echo-BEST.html'));
});

// Health check
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`The Mirror's Echo running on port ${PORT}`);
});
