# Railway Deployment Guide

## Deploy Unified HTTP+WebSocket Server to Railway

This guide will help you deploy the unified server (static files + WebSocket signaling) to Railway so you can access it from anywhere.

### Prerequisites

- A Railway account (sign up at https://railway.app)
- Git installed on your machine
- This repository cloned locally

### Step 1: Prepare for Deployment

The unified server is already configured to work with Railway:
- **Single Port**: Both HTTP (static files) and WebSocket (signaling at /ws) run on the same port
- **Health Check**: GET /healthz endpoint for Railway health monitoring
- **Auto-configuration**: Railway will automatically use the PORT environment variable
- **Config as Code**: railway.json specifies the start command and health check path

### Step 2: Deploy to Railway

#### Option A: Deploy via Railway CLI

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize a new Railway project in the repository:
```bash
cd /path/to/liquid-milk-balls-web
railway init
```

4. Deploy the signaling server:
```bash
railway up
```

5. Get your deployment URL:
```bash
railway domain
```

#### Option B: Deploy via Railway Dashboard

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select this repository: `kfaist/liquid-milk-balls-web`
4. **Important**: Select the branch with the unified server (main or the merged branch)
5. Railway will automatically:
   - Detect it's a Node.js project
   - Use railway.json for configuration
   - Run `node server.js` as the start command
   - Enable health checks at /healthz
6. Once deployed, click "Generate Domain" to get a public URL

### Step 3: Configure Railway Service Settings

In your Railway project dashboard:

#### Deployment Source
- **Source**: GitHub → `kfaist/liquid-milk-balls-web`
- **Branch**: `main` (or the branch with the unified server)

#### Build System
- Leave as default (Nixpacks) - railway.json specifies this

#### Start Command
- Automatically picked up from railway.json: `node server.js`
- You can verify this in Settings → Deploy → Start Command

#### Health Check (Configured in railway.json)
- Path: `/healthz`
- This is automatically configured via railway.json
- You can verify it's working by visiting: `https://your-app.up.railway.app/healthz`

#### Sleep Mode (Optional)
- If you want WebSocket connections to stay available 24/7, disable sleep mode
- Settings → Service → Sleep Mode → Disable

### Step 3: Verify Configuration

After deploying to Railway, you'll get a URL like: `https://your-app-name.up.railway.app`

**No configuration changes needed!** The app is already configured to automatically detect the correct WebSocket URL:
- `config.js` now dynamically determines the WebSocket URL based on your current location
- On Railway (HTTPS): automatically uses `wss://your-app-name.up.railway.app/ws`
- On localhost (HTTP): automatically uses `ws://localhost:3000/ws`

### Step 4: Test the Deployment

#### A. Test HTTP (Static Files)
1. Open the root page: `https://your-app.up.railway.app/`
   - Should serve your interactive mirror website
2. Test health check: `https://your-app.up.railway.app/healthz`
   - Should return: `ok`

#### B. Test WebSocket (Signaling)
From a terminal:
```bash
npx wscat -c wss://your-app.up.railway.app/ws
```
- Should connect successfully
- Type a message and press enter
- Open another terminal and connect again - messages should relay between clients

#### C. Test WebRTC in Browser
1. Open `https://your-app.up.railway.app/` in your browser
2. Click "Start Camera" (grant camera permissions)
3. Click "Start WebRTC Call"
4. Status should show "Connected to signaling server"
5. Open another browser window/tab and repeat steps 2-3
6. You should establish a peer-to-peer WebRTC connection

### Environment Variables (Optional)

Railway automatically provides these variables:
- `PORT` - The port your app should listen on
- `RAILWAY_STATIC_URL` - Your app's public URL

No additional configuration needed!

### Monitoring

View logs in real-time:
```bash
railway logs
```

Or check the Railway dashboard for metrics and logs.

### Costs

Railway offers:
- **Hobby Plan**: Free tier with $5 credit/month (sufficient for signaling server)
- **Pro Plan**: $20/month for higher usage

The signaling server is very lightweight and should easily fit within the free tier for development/testing.

### Security Notes

⚠️ **Important**: This signaling server is a simple relay without authentication. For production use, you should:

1. Add authentication (API keys, JWT tokens)
2. Implement rate limiting
3. Add CORS protection
4. Use proper WebSocket security
5. Consider using a managed service like Twilio or PubNub for production

### Troubleshooting

**Connection fails:**
- Verify Railway deployment is running: Check Railway dashboard
- Ensure you're using `wss://` (not `ws://`) for the deployed URL
- Check browser console for error messages

**WebRTC not connecting:**
- The signaling server only relays messages
- WebRTC connections still use STUN/TURN servers
- For connections outside local network, you may need TURN servers

### Alternative: Quick Deploy Button

Add this to your GitHub README for one-click deployment:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/kfaist/liquid-milk-balls-web)

### Configuring LiveKit (Optional)

If you want to use LiveKit instead of simple peer-to-peer WebRTC:

1. Set environment variables in Railway dashboard:
   - `LIVEKIT_API_KEY`: Your LiveKit API key
   - `LIVEKIT_API_SECRET`: Your LiveKit API secret
   - `LIVEKIT_URL`: Your LiveKit WebSocket URL (e.g., `wss://your-project.livekit.cloud`)
   - `LIVEKIT_ROOM_NAME`: Optional, defaults to `claymation-live`

2. Redeploy the service

3. Access the LiveKit viewer at: `https://your-app.up.railway.app/ndi-viewer.html`

See [WEBRTC-SETUP.md](WEBRTC-SETUP.md) for detailed LiveKit setup instructions.

### Next Steps

After deploying to Railway:
1. Test both simple WebRTC and LiveKit modes (if configured)
2. Try the complete workflow with OBS and TouchDesigner
3. Share the deployed web app URL with others!
4. For production use, consider adding authentication and rate limiting
