require('dotenv').config();
const express = require('express');
const path = require('path');
const { WebSocketServer } = require('ws');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { mountTurnEndpoint } = require('./turn-credentials');

const app = express();
const PORT = process.env.PORT || 3000;
const DOMAIN = process.env.DOMAIN || `http://localhost:${PORT}`;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '..')));

// Health check
app.get('/healthz', (req, res) => res.status(200).send('ok'));

/**
 * Stripe Configuration Endpoint
 * GET /api/stripe-config
 * 
 * Returns the Stripe publishable key for client-side Stripe.js initialization
 */
app.get('/api/stripe-config', (req, res) => {
  const publishableKey = process.env.STRIPE_PUBLISHABLE_KEY;

  if (!publishableKey) {
    console.error('[Stripe] STRIPE_PUBLISHABLE_KEY not configured');
    return res.status(500).json({
      error: 'Payment system not configured'
    });
  }

  res.json({
    publishableKey: publishableKey
  });
});

/**
 * Create Stripe Checkout Session
 * POST /api/create-checkout-session
 * 
 * Creates a Stripe Checkout session for the $400 Exhibition License
 * Returns the checkout URL or session ID for redirect
 * 
 * Environment variables required:
 * - STRIPE_SECRET_KEY: Stripe secret key (test or live)
 * - STRIPE_PUBLISHABLE_KEY: Stripe publishable key (optional, for embedded checkout)
 * - DOMAIN: Full domain URL for success/cancel redirects
 */
app.post('/api/create-checkout-session', async (req, res) => {
  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
  const STRIPE_PUBLISHABLE_KEY = process.env.STRIPE_PUBLISHABLE_KEY;

  if (!STRIPE_SECRET_KEY) {
    console.error('[Stripe] STRIPE_SECRET_KEY not configured');
    return res.status(500).json({
      error: 'Payment system not configured. Contact artist for licensing.',
      message: 'STRIPE_SECRET_KEY environment variable is required'
    });
  }

  try {
    // Determine success and cancel URLs
    const successUrl = `${DOMAIN}/payment-success.html?session_id={CHECKOUT_SESSION_ID}`;
    const cancelUrl = `${DOMAIN}/payment-cancel.html`;

    console.log('[Stripe] Creating checkout session:', {
      successUrl,
      cancelUrl
    });

    // Create Stripe Checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: 'Exhibition License - The Mirror\'s Echo',
              description: 'Commercial exhibition rights for The Mirror\'s Echo art installation. Includes unlimited sustained experience with no temporal markers.',
              images: [], // Add product images if available
            },
            unit_amount: 40000, // $400.00 in cents
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: successUrl,
      cancel_url: cancelUrl,
      metadata: {
        license_type: 'exhibition',
        product: 'mirrors-echo',
      },
      // Optional: Collect customer information
      customer_email: req.body.email || undefined,
    });

    console.log('[Stripe] Checkout session created:', session.id);

    // Return both sessionId and checkoutUrl for flexibility
    res.json({
      sessionId: session.id,
      checkoutUrl: session.url,
      publishableKey: STRIPE_PUBLISHABLE_KEY
    });

  } catch (error) {
    console.error('[Stripe] Error creating checkout session:', error);
    res.status(500).json({
      error: 'Failed to create checkout session',
      message: error.message
    });
  }
});

/**
 * Stripe Webhook Handler (optional, for future use)
 * POST /api/stripe-webhook
 * 
 * Handle Stripe webhook events for payment processing
 * Requires STRIPE_WEBHOOK_SECRET environment variable
 */
app.post('/api/stripe-webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  if (!webhookSecret) {
    console.warn('[Stripe] Webhook received but STRIPE_WEBHOOK_SECRET not configured');
    return res.status(400).send('Webhook secret not configured');
  }

  try {
    const event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);

    console.log('[Stripe] Webhook event:', event.type);

    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object;
        console.log('[Stripe] Payment successful:', session.id);
        // TODO: Fulfill the order, send license email, etc.
        break;
      case 'payment_intent.succeeded':
        const paymentIntent = event.data.object;
        console.log('[Stripe] PaymentIntent successful:', paymentIntent.id);
        break;
      default:
        console.log('[Stripe] Unhandled event type:', event.type);
    }

    res.json({ received: true });
  } catch (err) {
    console.error('[Stripe] Webhook error:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
});

// Mount TURN credentials endpoint
mountTurnEndpoint(app);

// WebSocket signaling server for WebRTC
// Uses path /signaling to match existing client code
const server = require('http').createServer(app);
const wss = new WebSocketServer({ server, path: '/signaling' });

// Track rooms: { roomName: Set<WebSocket> }
const rooms = new Map();

wss.on('connection', (ws) => {
  console.log('[WS] Client connected');
  ws.currentRoom = null;

  const keepalive = setInterval(() => {
    try {
      if (ws.readyState === ws.OPEN) {
        ws.ping();
      }
    } catch (e) {
      console.error('[WS] Ping error:', e);
    }
  }, 25000);

  ws.on('message', (msg) => {
    try {
      const data = JSON.parse(msg);

      // Handle room join
      if (data.type === 'join' || data.type === 'join-room') {
        const roomName = data.room || 'mirrors-echo-default';

        // Leave old room if exists
        if (ws.currentRoom && rooms.has(ws.currentRoom)) {
          rooms.get(ws.currentRoom).delete(ws);
          console.log(`[WS] Client left room: ${ws.currentRoom}`);
        }

        // Join new room
        if (!rooms.has(roomName)) {
          rooms.set(roomName, new Set());
        }
        rooms.get(roomName).add(ws);
        ws.currentRoom = roomName;
        console.log(`[WS] Client joined room: ${roomName} (${rooms.get(roomName).size} clients)`);

        // Notify client of successful join
        ws.send(JSON.stringify({ type: 'joined', room: roomName }));

        // If there's already another peer, notify initiator to start call
        if (rooms.get(roomName).size === 2) {
          ws.send(JSON.stringify({ type: 'ready' }));
        }

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
            console.error('[WS] Send error:', e);
          }
        }
      }
    } catch (e) {
      console.error('[WS] Message parsing error:', e);
    }
  });

  ws.on('close', () => {
    console.log('[WS] Client disconnected');

    // Remove from room
    if (ws.currentRoom && rooms.has(ws.currentRoom)) {
      rooms.get(ws.currentRoom).delete(ws);
      console.log(`[WS] Client removed from room: ${ws.currentRoom}`);

      // Clean up empty rooms
      if (rooms.get(ws.currentRoom).size === 0) {
        rooms.delete(ws.currentRoom);
        console.log(`[WS] Room deleted: ${ws.currentRoom}`);
      }
    }

    clearInterval(keepalive);
  });

  ws.on('error', (error) => {
    console.error('[WS] WebSocket error:', error);
  });
});

// Start server
server.listen(PORT, '0.0.0.0', () => {
  console.log('═══════════════════════════════════════════════════════');
  console.log('🎭  Mirror\'s Echo - Production Server');
  console.log('═══════════════════════════════════════════════════════');
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`📺 Main page: ${DOMAIN}`);
  console.log(`🔌 WebSocket: ws://localhost:${PORT}/signaling`);
  console.log('───────────────────────────────────────────────────────');

  // Check Stripe configuration
  if (process.env.STRIPE_SECRET_KEY && process.env.STRIPE_PUBLISHABLE_KEY) {
    console.log('💳 Stripe Payment: CONFIGURED');
    console.log('   /api/stripe-config');
    console.log('   /api/create-checkout-session');
  } else {
    console.log('⚠️  Stripe Payment: NOT CONFIGURED');
    console.log('   Set STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY');
  }

  // Check TURN configuration
  if (process.env.TURN_SECRET && process.env.TURN_SERVER_URL) {
    console.log('🔄 TURN Server: CONFIGURED');
    console.log(`   /api/turn-credentials -> ${process.env.TURN_SERVER_URL}`);
  } else {
    console.log('⚠️  TURN Server: NOT CONFIGURED');
    console.log('   Set TURN_SECRET and TURN_SERVER_URL');
  }

  console.log('═══════════════════════════════════════════════════════');
});

module.exports = app;
