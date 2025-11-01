/**
 * LiveKit Token Mint Endpoint
 * 
 * This endpoint mints LiveKit access tokens server-side.
 * 
 * SECURITY NOTES:
 * - LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in server environment
 * - NEVER expose these credentials to clients
 * - requireAuth is a stub - wire to your actual auth system
 * - In production, verify Stripe/billing status before allowing publish permissions
 */

const { AccessToken } = require('livekit-server-sdk');

/**
 * Auth middleware stub
 * 
 * TODO: Replace with actual authentication
 * - Verify JWT/session token
 * - Check user permissions
 * - Verify billing/subscription status via Stripe
 * 
 * @param {object} req - Express request
 * @param {object} res - Express response
 * @param {function} next - Express next middleware
 */
function requireAuth(req, res, next) {
  // STUB: This is a placeholder auth check
  // In production, replace with:
  // - JWT verification
  // - Session validation
  // - Database user lookup
  
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ 
      error: 'Unauthorized',
      message: 'Authorization header required'
    });
  }

  // STUB: Extract and validate token
  // const token = authHeader.split(' ')[1];
  // const user = await verifyToken(token); // Implement this
  
  // For now, attach a stub user
  req.user = {
    id: 'stub-user-id',
    username: 'test-user',
    // In production, check:
    // - hasActiveSubscription
    // - publishingEnabled
    // - role/permissions
  };
  
  next();
}

/**
 * POST /api/join
 * Mint a LiveKit access token for a room
 * 
 * Request body:
 * {
 *   "room": "room-name",
 *   "username": "optional-display-name"
 * }
 * 
 * Response:
 * {
 *   "token": "ey...",
 *   "url": "wss://your-livekit-server.com",
 *   "ttl": 3600
 * }
 */
async function joinRoom(req, res) {
  try {
    const { room, username } = req.body;
    
    // Validate input
    if (!room) {
      return res.status(400).json({ 
        error: 'Bad Request',
        message: 'room is required'
      });
    }

    // Validate environment
    const apiKey = process.env.LIVEKIT_API_KEY;
    const apiSecret = process.env.LIVEKIT_API_SECRET;
    const livekitUrl = process.env.LIVEKIT_URL || 'wss://your-livekit-server.com';

    if (!apiKey || !apiSecret) {
      console.error('[join] LIVEKIT_API_KEY or LIVEKIT_API_SECRET not configured');
      return res.status(500).json({ 
        error: 'Server Configuration Error',
        message: 'LiveKit credentials not configured'
      });
    }

    // Get user identity from auth
    const identity = req.user.id;
    const displayName = username || req.user.username;

    // Create access token
    const token = new AccessToken(apiKey, apiSecret, {
      identity,
      name: displayName,
      // Token valid for 1 hour
      ttl: 3600,
    });

    // Grant permissions
    // IMPORTANT: In production, check user's subscription/billing status
    // before granting publish permissions
    
    // TODO: Add Stripe billing check here
    // const subscription = await getStripeSubscription(req.user.id);
    // const canPublish = subscription.active && subscription.plan.features.includes('publish');
    
    // For now, grant view-only by default (safe default)
    // Set canPublish: true only for paid/authorized users
    token.addGrant({
      room,
      roomJoin: true,
      canPublish: false,  // TODO: Set based on billing/subscription
      canSubscribe: true,
      canPublishData: false,
    });

    const jwt = await token.toJwt();

    res.json({
      token: jwt,
      url: livekitUrl,
      ttl: 3600,
      room,
      identity,
    });

  } catch (error) {
    console.error('[join] Error minting token:', error);
    res.status(500).json({ 
      error: 'Internal Server Error',
      message: 'Failed to mint token'
    });
  }
}

module.exports = {
  requireAuth,
  joinRoom,
};
