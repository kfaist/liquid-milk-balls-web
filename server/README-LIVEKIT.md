# LiveKit Integration Setup

This document describes how to set up the LiveKit token mint endpoint for secure WebRTC connections.

## Overview

The `/api/join` endpoint mints LiveKit access tokens server-side. This is required because:

1. **Security**: LiveKit API credentials must never be exposed to clients
2. **Authorization**: Server can verify auth and billing before granting access
3. **Control**: Server controls room permissions (publish, subscribe, etc.)

## Environment Variables

Configure these in your Railway/hosting environment:

### Required

```bash
# LiveKit API credentials (get from LiveKit Cloud dashboard)
LIVEKIT_API_KEY=your-api-key-here
LIVEKIT_API_SECRET=your-api-secret-here

# LiveKit server URL
LIVEKIT_URL=wss://your-project.livekit.cloud
```

### Optional

```bash
# Port for the server (Railway sets this automatically)
PORT=3000
```

## Getting LiveKit Credentials

1. Sign up at [https://cloud.livekit.io](https://cloud.livekit.io)
2. Create a new project
3. Go to Settings → Keys
4. Create an API key pair (key + secret)
5. Copy the credentials to your environment variables

**IMPORTANT**: Never commit these credentials to git or expose them to clients!

## Railway Setup

In your Railway project:

1. Go to your service → Variables
2. Add the three environment variables listed above
3. Click "Deploy" or wait for auto-deploy

Railway will automatically redeploy with the new environment variables.

## Local Development

Create a `.env` file (already in .gitignore):

```bash
LIVEKIT_API_KEY=your-dev-api-key
LIVEKIT_API_SECRET=your-dev-api-secret
LIVEKIT_URL=wss://your-project.livekit.cloud
PORT=3000
```

Then use `dotenv`:

```bash
npm install dotenv
node -r dotenv/config server.js
```

Or set environment variables directly:

```bash
export LIVEKIT_API_KEY=your-key
export LIVEKIT_API_SECRET=your-secret
export LIVEKIT_URL=wss://your-url
npm start
```

## API Endpoint

### POST /api/join

Mint a LiveKit access token for a room.

**Request:**

```bash
curl -X POST http://localhost:3000/api/join \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-auth-token" \
  -d '{"room": "test-room", "username": "Alice"}'
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "url": "wss://your-project.livekit.cloud",
  "ttl": 3600,
  "room": "test-room",
  "identity": "user-id"
}
```

**Error Responses:**

- `401 Unauthorized` - Missing or invalid auth token
- `400 Bad Request` - Missing room parameter
- `500 Server Error` - LiveKit credentials not configured or token generation failed

## Authentication

The `requireAuth` middleware in `server/api/join.js` is currently a **stub**.

### Production Implementation

Before deploying to production, replace the stub with real authentication:

```javascript
// Example with JWT
const jwt = require('jsonwebtoken');

function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const token = authHeader.split(' ')[1];
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Billing Integration

Before granting `canPublish: true`, verify the user's subscription:

```javascript
// Example Stripe check
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

async function joinRoom(req, res) {
  // ... existing code ...
  
  // Check subscription before granting publish permissions
  const subscription = await stripe.subscriptions.retrieve(
    req.user.subscriptionId
  );
  
  const canPublish = subscription.status === 'active' && 
                     subscription.plan.metadata.features.includes('publish');
  
  token.addGrant({
    room,
    roomJoin: true,
    canPublish,  // Based on subscription
    canSubscribe: true,
  });
  
  // ... rest of code ...
}
```

## Security Checklist

Before going to production:

- [ ] LIVEKIT_API_KEY and LIVEKIT_API_SECRET are set in Railway environment
- [ ] Credentials are NOT in code or client-accessible files
- [ ] requireAuth middleware is replaced with real auth
- [ ] User permissions are verified (subscription/billing check)
- [ ] canPublish is false by default (safe default)
- [ ] canPublish only granted to paid/authorized users
- [ ] JWT_SECRET or session secret is configured
- [ ] HTTPS is enforced (Railway does this automatically)
- [ ] Rate limiting is configured (optional but recommended)

## Testing

### 1. Test Token Generation

With the server running and environment variables set:

```bash
# Test with stub auth
curl -X POST http://localhost:3000/api/join \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer stub-token" \
  -d '{"room": "test-room"}'
```

Expected: JSON response with token, url, ttl

### 2. Test LiveKit Connection

Use the client snippet (see client/livekit-join.js) or LiveKit's test page:

```javascript
import { Room } from 'livekit-client';

const room = new Room();
await room.connect(url, token);
console.log('Connected to room:', room.name);
```

### 3. Verify No Credential Leakage

Check that credentials don't appear in:
- Client-side JavaScript bundles
- Browser network inspector
- Console logs
- Error messages

```bash
# Check client files for secrets
grep -r "LIVEKIT_API_SECRET" client/ public/ static/
# Should return no results
```

## Troubleshooting

### "LiveKit credentials not configured"

- Verify LIVEKIT_API_KEY and LIVEKIT_API_SECRET are set
- Restart the server after setting environment variables
- Check Railway logs for startup errors

### "Invalid token" from LiveKit

- Verify LIVEKIT_API_KEY and LIVEKIT_API_SECRET match your LiveKit project
- Check that LIVEKIT_URL points to the correct server
- Ensure token hasn't expired (default 1 hour TTL)

### "Unauthorized" error

- The requireAuth middleware requires an Authorization header
- Replace stub auth with real authentication before production use

## Next Steps

1. Set up LiveKit Cloud account and credentials
2. Configure environment variables in Railway
3. Implement real authentication (replace stub)
4. Add Stripe billing checks
5. Test end-to-end flow
6. Deploy to production

## Resources

- [LiveKit Documentation](https://docs.livekit.io)
- [LiveKit Server SDK](https://github.com/livekit/server-sdk-js)
- [LiveKit Client SDK](https://github.com/livekit/client-sdk-js)
- [Railway Docs](https://docs.railway.app)
