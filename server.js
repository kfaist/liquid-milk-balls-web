const express = require('express');
const path = require('path');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const PORT = process.env.PORT || 3000;

const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';

// Serve static files
app.use(express.static(__dirname));

// Generate LiveKit token for publisher/subscriber
app.get('/token', async (req, res) => {
    const roomName = req.query.room || 'claymation-live';
    const identity = req.query.identity || 'user-' + Math.random().toString(36).substr(2, 6);
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
        
        const jwt = await token.toJwt();
        
        console.log('Generated token for', identity, 'in room', roomName, 'publisher:', isPublisher);
        
        res.json({ 
            token: jwt,
            url: LIVEKIT_URL,
            room: roomName,
            identity: identity
        });
    } catch (error) {
        console.error('Token generation error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Generate OBS WHIP token for ingress (processed video return)
app.get('/obs-whip-token', async (req, res) => {
    const roomName = req.query.room || 'claymation-live';
    const streamName = req.query.stream || 'obs-processed';
    
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
            identity: streamName,
            ttl: '24h'
        });
        
        token.addGrant({
            room: roomName,
            roomJoin: true,
            canPublish: true,
            canSubscribe: false
        });
        
        const jwt = await token.toJwt();
        
        // LiveKit WHIP endpoint format
        const whipUrl = 'https://claymation-transcription-l6e51sws.livekit.cloud/w';
        
        console.log('Generated OBS WHIP token for', streamName, 'in room', roomName);
        
        res.json({
            whip_url: whipUrl,
            bearer_token: jwt,
            room: roomName,
            stream_name: streamName,
            instructions: 'In OBS: Settings → Stream → Service: WHIP, Server: ' + whipUrl + ', Bearer Token: (use bearer_token above)'
        });
    } catch (error) {
        console.error('WHIP token generation error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Main route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'mirrors-echo-vibrant.html'));
});

// Health check
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`The Mirror's Echo running on port ${PORT}`);
    console.log(`WHIP token endpoint: http://localhost:${PORT}/obs-whip-token?room=claymation-live`);
});
