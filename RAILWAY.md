# Railway Deployment Guide

## Deploy WebRTC Signaling Server to Railway

This guide will help you deploy the WebRTC signaling server to Railway so you can access it from anywhere.

### Prerequisites

- A Railway account (sign up at https://railway.app)
- Git installed on your machine
- This repository cloned locally

### Step 1: Prepare for Deployment

The signaling server is already configured to work with Railway. It will automatically use the PORT environment variable that Railway provides.

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
3. Select this repository
4. Railway will automatically detect it's a Node.js project
5. The deployment will start automatically
6. Once deployed, click "Generate Domain" to get a public URL

### Step 3: Configure the Web App

After deploying to Railway, you'll get a URL like: `https://your-app-name.up.railway.app`

1. Open `config.js` in your local repository
2. Update the `SIGNALING_SERVER_URL` to use your Railway URL with `wss://`:
```javascript
window.SIGNALING_SERVER_URL = 'wss://your-app-name.up.railway.app';
```

3. Commit and push the changes (or deploy the static files to GitLab Pages/Vercel/Netlify)

### Step 4: Test the Deployment

1. Open your web app (either locally or on GitLab Pages)
2. Click "Start Camera"
3. Click "Start WebRTC Call"
4. The status should show "Connected to signaling server"
5. Open another browser window/tab and repeat - you should establish a peer connection

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

### Next Steps

After deploying the signaling server:
1. Deploy the web app to GitLab Pages (already configured) or another host
2. Update `config.js` with your Railway WebSocket URL
3. Test the complete workflow with OBS and TouchDesigner
4. Share the deployed web app URL with others!
