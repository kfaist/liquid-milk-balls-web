const express = require('express');
const path = require('path');
const { AccessToken, RoomServiceClient } = require('livekit-server-sdk');

const app = express();
const PORT = process.env.PORT || 3000;

const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_URL = 'https://claymation-transcription-l6e51sws.livekit.cloud';

// Room Service Client for checking/managing participants
const roomService = new RoomServiceClient(LIVEKIT_API_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

// Stripe configuration
const STRIPE_PUBLISHABLE_KEY = process.env.STRIPE_PUBLISHABLE_KEY || '';
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || '';
const stripe = STRIPE_SECRET_KEY ? require('stripe')(STRIPE_SECRET_KEY) : null;

// Middleware
app.use(express.json());
app.use(express.static(__dirname));

// ============================================
// ROOM STATUS - Check if room has capacity
// ============================================
app.get('/api/room-status', async (req, res) => {
    const room = req.query.room || 'claymation-live';
    try {
        const participants = await roomService.listParticipants(room);
        // Count only mirror-users (not transcriber, not viewer, not obs)
        const mirrorUsers = participants.filter(p => 
            p.identity.startsWith('mirror-user') && 
            !p.identity.startsWith('transcriber') &&
            !p.identity.startsWith('viewer') &&
            !p.identity.startsWith('obs')
        );
        res.json({
            room,
            mirrorUserCount: mirrorUsers.length,
            available: mirrorUsers.length === 0,
            allParticipants: participants.map(p => p.identity)
        });
    } catch (error) {
        // Room doesn't exist = available
        if (error.message && error.message.includes('not found')) {
            res.json({ room, mirrorUserCount: 0, available: true, allParticipants: [] });
        } else {
            console.error('Room status error:', error);
            res.status(500).json({ error: error.message });
        }
    }
});

// ============================================
// KICK USER - Force remove a participant
// ============================================
app.post('/api/kick-user', async (req, res) => {
    const { room, identity } = req.body;
    if (!room || !identity) {
        return res.status(400).json({ error: 'room and identity required' });
    }
    try {
        await roomService.removeParticipant(room, identity);
        console.log(`Kicked ${identity} from ${room}`);
        res.json({ success: true, kicked: identity });
    } catch (error) {
        console.error('Kick error:', error);
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// CLEANUP ZOMBIES - Remove old transcribers/mirror-users
// ============================================
app.post('/api/cleanup-room', async (req, res) => {
    const room = req.body.room || 'claymation-live';
    try {
        const participants = await roomService.listParticipants(room);
        let removed = [];
        for (const p of participants) {
            // Remove old-style timestamp-based transcribers (keep transcriber-main)
            if (p.identity.startsWith('transcriber-') && p.identity !== 'transcriber-main') {
                await roomService.removeParticipant(room, p.identity);
                removed.push(p.identity);
            }
            // Remove old-style mirror-users (keep mirror-user-active)
            if (p.identity.startsWith('mirror-user-') && p.identity !== 'mirror-user-active') {
                await roomService.removeParticipant(room, p.identity);
                removed.push(p.identity);
            }
            // Remove old-style viewers (keep viewer-td)
            if (p.identity.startsWith('viewer-') && p.identity !== 'viewer-td') {
                await roomService.removeParticipant(room, p.identity);
                removed.push(p.identity);
            }
        }
        console.log(`Cleaned up ${removed.length} zombies from ${room}:`, removed);
        res.json({ success: true, removed, count: removed.length });
    } catch (error) {
        if (error.message && error.message.includes('not found')) {
            res.json({ success: true, removed: [], count: 0, message: 'Room empty' });
        } else {
            console.error('Cleanup error:', error);
            res.status(500).json({ error: error.message });
        }
    }
});

// ============================================
// TOKEN ENDPOINTS
// ============================================

// Publisher token - FIXED IDENTITY, ONE USER LIMIT
app.get('/api/publisher-token', async (req, res) => {
    const identity = 'mirror-user-active';  // FIXED - auto-kicks previous
    try {
        // Check if someone else is already connected
        try {
            const participants = await roomService.listParticipants('claymation-live');
            const existingMirrorUser = participants.find(p => p.identity === identity);
            if (existingMirrorUser) {
                // Kick the old one (stale session)
                await roomService.removeParticipant('claymation-live', identity);
                console.log('Kicked stale mirror-user-active');
            }
        } catch (e) {
            // Room doesn't exist yet, that's fine
        }

        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { 
            identity, 
            ttl: '15m'  // Shorter TTL
        });
        token.addGrant({ 
            room: 'claymation-live', 
            roomJoin: true, 
            canPublish: true, 
            canSubscribe: false 
        });
        console.log('Issued publisher token for mirror-user-active');
        res.json({ token: await token.toJwt(), url: LIVEKIT_URL, room: 'claymation-live', identity });
    } catch (e) { 
        console.error('Publisher token error:', e);
        res.status(500).json({ error: e.message }); 
    }
});

// Viewer token for TD (subscribes to claymation-live) - FIXED IDENTITY
app.get('/api/viewer-token', async (req, res) => {
    const identity = 'viewer-td';  // FIXED - for TouchDesigner WebRender
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '24h' });
        token.addGrant({ room: 'claymation-live', roomJoin: true, canPublish: false, canSubscribe: true });
        res.json({ token: await token.toJwt(), url: LIVEKIT_URL, room: 'claymation-live' });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

// Processed viewer token (subscribes to processed-output) - FIXED IDENTITY
app.get('/api/processed-viewer-token', async (req, res) => {
    const identity = 'mirror-viewer-active';  // FIXED - matches the one publisher
    try {
        const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity, ttl: '15m' });
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

// Legacy /token endpoint
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
        console.log('Legacy token for', identity, 'in room', roomName);
        
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

// OBS WHIP token
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
        const whipUrl = 'https://claymation-transcription-l6e51sws.livekit.cloud/w';
        
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

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'mirrors-echo-fixed.html'));
});

// ============================================
// STRIPE ENDPOINTS
// ============================================
app.get('/api/stripe-config', (req, res) => {
    if (!STRIPE_PUBLISHABLE_KEY) {
        return res.status(503).json({ error: 'Stripe not configured' });
    }
    res.json({ publishableKey: STRIPE_PUBLISHABLE_KEY });
});

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
                    unit_amount: 40000,
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
    console.log(`Fixed identities: mirror-user-active, viewer-td, mirror-viewer-active, transcriber-main`);
});
