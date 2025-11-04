# Quick Start Guide

## 🎯 Goal
Get live webcam video from any browser into OBS → NDI → TouchDesigner → and optionally back to browser.

## ⚡ Fast Setup (5 minutes)

### Prerequisites
- ✅ Node.js installed
- ✅ LiveKit account (get free at [livekit.io](https://livekit.io))
- ✅ OBS Studio with obs-ndi plugin
- ✅ NDI Runtime installed
- ✅ TouchDesigner

### Step 1: Configure LiveKit (2 minutes)

```bash
# Set environment variables (or create .env file)
export LIVEKIT_API_KEY="your-api-key-here"
export LIVEKIT_API_SECRET="your-api-secret-here"
export LIVEKIT_URL="wss://your-project.livekit.cloud"
```

### Step 2: Start Server (30 seconds)

```bash
npm install
npm start
```

You should see:
```
[server] HTTP+WS listening on :3000
[server] LiveKit configured for room: claymation-live
```

### Step 3: Publish Webcam (1 minute)

Open in browser (or send to remote user):
```
http://localhost:3000/publisher.html
```

Click **"Start Publishing"** → Grant camera permission

### Step 4: Setup OBS (1 minute)

1. Add **Browser Source**
2. URL: `http://localhost:3000/ndi-viewer.html`
3. Width: 1920, Height: 1080
4. Go to **Tools** → **NDI Output Settings**
5. Enable **"Main Output"**

### Step 5: Receive in TouchDesigner (30 seconds)

1. Add **NDI In TOP** operator
2. Select your OBS NDI source from dropdown
3. You're done! 🎉

## 🌐 Remote Access

### Deploy to Railway (for internet access)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Add variables in Railway dashboard:
# LIVEKIT_API_KEY
# LIVEKIT_API_SECRET
# LIVEKIT_URL
# LIVEKIT_ROOM_NAME
```

Then use `https://your-app.up.railway.app/publisher.html` instead of localhost.

## 📖 Key Pages

| Page | Purpose | Who Uses It |
|------|---------|-------------|
| **publisher.html** | Publish webcam to LiveKit | Remote user with camera |
| **ndi-viewer.html** | View LiveKit stream | OBS Browser Source |
| **index.html** | Landing page with info | Entry point |
| **viewer.html** | P2P testing viewer | Local testing only |

## 🔄 The Complete Loop

```
┌──────────────┐
│ Browser      │  📹 Webcam
│ publisher    │──────────────┐
└──────────────┘              │
                              ▼
                      ┌───────────────┐
                      │ LiveKit Cloud │
                      └───────┬───────┘
                              │
                              ▼
┌──────────────┐      ┌──────────────┐
│ OBS          │◄─────│ ndi-viewer   │
│ Browser Src  │      │ (browser)    │
└──────┬───────┘      └──────────────┘
       │
       │ NDI Output
       ▼
┌──────────────┐
│ TouchDesigner│  🎨 Process
│ NDI In TOP   │──────────────┐
└──────────────┘              │
                              ▼
                      ┌──────────────┐
                      │ Output       │
                      │ • Screen     │
                      │ • Projector  │
                      │ • Back to    │
                      │   LiveKit    │
                      └──────────────┘
```

## 🐛 Troubleshooting

### "LiveKit not configured"
➜ Set environment variables and restart server

### "Failed to get token"
➜ Check LiveKit credentials are correct

### Camera permission denied
➜ Must use `http://localhost` or `https://`, click Allow in browser

### No video in OBS
➜ Verify publisher is streaming, refresh Browser Source in OBS

### NDI not showing in TouchDesigner
➜ Check NDI Output is enabled in OBS, restart TouchDesigner

## 📚 More Info

- **Full Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Detailed Setup**: See [WEBRTC-SETUP.md](WEBRTC-SETUP.md)
- **LiveKit Guide**: See [LIVEKIT-SETUP-GUIDE.md](LIVEKIT-SETUP-GUIDE.md)

## 💡 Pro Tips

- **Multiple Cameras**: Open publisher.html on multiple devices, all stream to same room
- **Quality**: Edit publisher.html line 236 to change resolution (h720 → h1080)
- **Local Testing**: Use simple WebRTC on index.html if you don't have LiveKit
- **Secure**: Always use HTTPS in production
- **Performance**: Lower resolution if experiencing lag

## 🆘 Need Help?

1. Check the server console for errors
2. Check browser console (F12) for JavaScript errors
3. Verify all environment variables are set
4. Try the simple WebRTC mode first (index.html)
5. Check [RAILWAY-TROUBLESHOOTING.md](RAILWAY-TROUBLESHOOTING.md) for deployment issues
