const crypto = require('crypto');

/**
 * TURN Credential Generation Module
 * 
 * Generates time-limited TURN credentials using HMAC-SHA1 authentication
 * compatible with coturn's use-auth-secret configuration.
 * 
 * The credentials are time-limited to prevent abuse and must be regenerated
 * periodically by the client.
 */

/**
 * Generate TURN credentials using HMAC-SHA1
 * @param {string} secret - The shared secret (must match coturn's static-auth-secret)
 * @param {number} ttl - Time to live in seconds (default: 3600 = 1 hour)
 * @param {string} turnServerUrl - TURN server URL (e.g., 'turn.example.com')
 * @returns {Object} Credentials object with username, credential, ttl, and urls
 */
function generateTurnCredentials(secret, ttl = 3600, turnServerUrl = 'turn.example.com') {
  if (!secret) {
    throw new Error('TURN secret is required');
  }

  // Generate username with expiration timestamp
  const timestamp = Math.floor(Date.now() / 1000) + ttl;
  const username = `${timestamp}:mirrors-echo-user`;

  // Generate HMAC-SHA1 credential
  const hmac = crypto.createHmac('sha1', secret);
  hmac.update(username);
  const credential = hmac.digest('base64');

  return {
    username,
    credential,
    ttl,
    urls: [
      `turn:${turnServerUrl}:3478?transport=udp`,
      `turn:${turnServerUrl}:3478?transport=tcp`,
      // Include TLS TURN if your server supports it
      // `turns:${turnServerUrl}:5349?transport=tcp`
    ]
  };
}

/**
 * Express route handler for /api/turn-credentials
 * 
 * Environment variables required:
 * - TURN_SECRET: The shared secret (must match coturn's static-auth-secret)
 * - TURN_SERVER_URL: The TURN server domain or IP (default: 'turn.example.com')
 * - TURN_TTL: Credential time-to-live in seconds (default: 3600)
 */
function turnCredentialsHandler(req, res) {
  const turnSecret = process.env.TURN_SECRET;
  const turnServerUrl = process.env.TURN_SERVER_URL || 'turn.example.com';
  const ttl = parseInt(process.env.TURN_TTL || '3600', 10);

  if (!turnSecret) {
    console.error('[TURN] TURN_SECRET environment variable not set');
    return res.status(500).json({
      error: 'TURN server not configured. Contact administrator.',
      message: 'TURN_SECRET environment variable is required'
    });
  }

  try {
    const credentials = generateTurnCredentials(turnSecret, ttl, turnServerUrl);
    
    console.log('[TURN] Generated credentials for client:', {
      username: credentials.username,
      ttl: credentials.ttl,
      urls: credentials.urls
    });

    res.json(credentials);
  } catch (error) {
    console.error('[TURN] Error generating credentials:', error);
    res.status(500).json({
      error: 'Failed to generate TURN credentials',
      message: error.message
    });
  }
}

/**
 * Mount TURN credentials endpoint on an Express app
 * @param {Express} app - Express application instance
 */
function mountTurnEndpoint(app) {
  app.get('/api/turn-credentials', turnCredentialsHandler);
  console.log('[TURN] Mounted /api/turn-credentials endpoint');
}

module.exports = {
  generateTurnCredentials,
  turnCredentialsHandler,
  mountTurnEndpoint
};
