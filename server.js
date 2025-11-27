const express = require('express');
const path = require('path');
const { AccessToken } = require('livekit-server-sdk');

const app = express();
const PORT = process.env.PORT || 3000;

const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';

// Stripe configuration (set these in Railway environment variables)
const STRIPE_PUBLISHABLE_KEY = process.env.STRIPE_PUBLISHABLE_KEY || '';
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || '';
const stripe = STRIPE_SECRET_KEY ? require('stripe')(STRIPE_SECRET_KEY) : null;

// Middleware
app.use(express.json());

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

// Main route - serve the dual-room experience
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'mirrors-echo-fixed.html'));
});

// API endpoints for mirrors-echo-fixed.html and td-input-viewer.html

// Viewer token (subscribes to claymation-live)
app.get('/api/viewer-token', async (req, res) => {
    const identity = 'viewer-' + Date.now();
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '6h' });
        token.addGrant({ room: 'claymation-live', roomJoin: true, canPublish: false, canSubscribe: true });
        res.json({ token: await token.toJwt(), url: LIVEKIT_URL, room: 'claymation-live' });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

// Publisher token (publishes to claymation-live)
app.get('/api/publisher-token', async (req, res) => {
    const identity = req.query.identity || 'publisher-' + Date.now();
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '6h' });
        token.addGrant({ room: 'claymation-live', roomJoin: true, canPublish: true, canSubscribe: false });
        res.json({ token: await token.toJwt(), url: LIVEKIT_URL, room: 'claymation-live' });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

// Processed viewer token (subscribes to processed-output)
app.get('/api/processed-viewer-token', async (req, res) => {
    const identity = req.query.identity || 'processed-viewer-' + Date.now();
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '6h' });
        token.addGrant({ room: 'processed-output', roomJoin: true, canPublish: false, canSubscribe: true });
        res.json({ token: await token.toJwt(), url: LIVEKIT_URL, room: 'processed-output' });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

// Processed publisher token (for OBS WHIP to processed-output)
app.get('/api/processed-publisher-token', async (req, res) => {
    const identity = 'obs-whip-publisher';
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '24h' });
        token.addGrant({ room: 'processed-output', roomJoin: true, canPublish: true, canSubscribe: false });
        const jwt = await token.toJwt();
        res.json({ 
            token: jwt, 
            url: LIVEKIT_URL, 
            room: 'processed-output',
            whipUrl: `https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token=${jwt}`
        });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

// ============================================
// STRIPE ENDPOINTS
// ============================================

// Get Stripe publishable key
app.get('/api/stripe-config', (req, res) => {
    if (!STRIPE_PUBLISHABLE_KEY) {
        return res.status(503).json({ error: 'Stripe not configured' });
    }
    res.json({ publishableKey: STRIPE_PUBLISHABLE_KEY });
});

// Create Stripe checkout session for $400 exhibition license
app.post('/api/create-checkout-session', async (req, res) => {
    if (!stripe) {
        return res.status(503).json({ error: 'Payment system not configured. Please contact kristabluedoor@gmail.com' });
    }
    
    try {
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: [{
                price_data: {
                    currency: 'usd',
                    product_data: {
                        name: 'The Mirror\'s Echo - Exhibition License',
                        description: 'Unlimited sustained experience, commercial exhibition rights, professional use licensing',
                    },
                    unit_amount: 40000, // $400.00 in cents
                },
                quantity: 1,
            }],
            mode: 'payment',
            success_url: `${req.protocol}://${req.get('host')}/licensing.html?success=true`,
            cancel_url: `${req.protocol}://${req.get('host')}/licensing.html?canceled=true`,
        });
        
        res.json({ sessionId: session.id });
    } catch (error) {
        console.error('Stripe checkout error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`The Mirror's Echo running on port ${PORT}`);
    console.log(`WHIP token endpoint: http://localhost:${PORT}/obs-whip-token?room=claymation-live`);
});
