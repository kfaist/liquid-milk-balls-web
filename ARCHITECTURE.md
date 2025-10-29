# 🏗️ Deployment Architecture

This document explains how the different components work together when deployed.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          LIVE SITE                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   Frontend (Web)     │         │   Backend (Server)   │
│                      │         │                      │
│  GitLab Pages /      │◄───────►│   Railway.app        │
│  Vercel / Netlify    │  WSS    │                      │
│                      │         │                      │
│  • index.html        │         │  • Node.js Server    │
│  • styles.css        │         │  • WebSocket (ws)    │
│  • script.js         │         │  • Port: Auto        │
│  • webrtc-client.js  │         │                      │
│  • config.js         │         │                      │
└──────────────────────┘         └──────────────────────┘
         │                                  │
         │                                  │
         └──────────────┬───────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   User Browser  │
              │                 │
              │  • WebRTC       │
              │  • Camera       │
              │  • Peer-to-Peer │
              └─────────────────┘
```

## Component Details

### Frontend (Static Web App)

**Files:**
- `index.html` - Main HTML page with interactive mirror UI
- `styles.css` - Styling with glassmorphism effects
- `script.js` - Mirror interaction logic
- `webrtc-client.js` - WebRTC connection handling
- `config.js` - Configuration (WebSocket URL)

**Hosting Options:**
1. **GitLab Pages** (Recommended)
   - URL: `https://username.gitlab.io/the-mirrors-echo/`
   - Auto-deploys via `.gitlab-ci.yml`
   - Free for public/private repos

2. **Vercel**
   - URL: `https://project-name.vercel.app`
   - Deploy with: `vercel`
   - Free tier available

3. **Netlify**
   - URL: `https://project-name.netlify.app`
   - Drag-and-drop or CLI deploy
   - Free tier available

**What it does:**
- Serves the interactive web interface
- Captures user camera via browser WebRTC API
- Connects to backend signaling server via WebSocket
- Establishes peer-to-peer WebRTC connections

### Backend (Signaling Server)

**File:**
- `webrtc-signaling-server.js` - WebSocket relay server

**Hosting:**
- **Railway.app**
  - URL: `https://your-app-name.up.railway.app`
  - Auto-detects Node.js via `package.json`
  - Uses `railway.json` for configuration
  - Free $5 credit/month

**What it does:**
- Relays WebRTC signaling messages (SDP offers/answers)
- Relays ICE candidates for NAT traversal
- Manages connected clients
- Does NOT handle actual video/audio data (that's peer-to-peer)

**Port Configuration:**
```javascript
const PORT = process.env.PORT || 8888;
```
Railway automatically sets `process.env.PORT`, so it works out of the box.

## Data Flow

### Initial Connection

```
1. User opens frontend URL
   └─► Browser loads HTML/CSS/JS

2. User clicks "Start Camera"
   └─► Browser requests camera permission
       └─► Camera stream available

3. User clicks "Start WebRTC Call"
   └─► Frontend connects to Railway WebSocket
       └─► config.js provides the WSS URL
           └─► Connection: wss://your-app.up.railway.app
```

### Peer Connection Setup

```
Browser A                 Railway Server              Browser B
   │                           │                         │
   │──── connect via WSS ──────►│                         │
   │                           │◄──── connect via WSS ────│
   │                           │                         │
   │──── SDP offer ───────────►│                         │
   │                           │──── relay offer ────────►│
   │                           │                         │
   │                           │◄──── SDP answer ─────────│
   │◄──── relay answer ────────│                         │
   │                           │                         │
   │──── ICE candidate ───────►│                         │
   │                           │──── relay candidate ────►│
   │                           │                         │
   │◄════ Direct P2P Connection ═══════════════════════►│
   │          (video/audio data)                        │
```

**Key Points:**
- Signaling goes through Railway server
- Actual media goes peer-to-peer (not through server)
- Uses STUN server for NAT traversal: `stun:stun.l.google.com:19302`

## Configuration Files

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"  // Auto-detects Node.js
  },
  "deploy": {
    "startCommand": "node webrtc-signaling-server.js",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `package.json` (relevant parts)
```json
{
  "main": "webrtc-signaling-server.js",
  "scripts": {
    "start": "node webrtc-signaling-server.js"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
```

### `config.js`
```javascript
// Before deployment (local testing)
window.SIGNALING_SERVER_URL = 'ws://localhost:8888';

// After deployment (production)
window.SIGNALING_SERVER_URL = 'wss://your-app-name.up.railway.app';
```

## Security Considerations

### Current Setup (Development/Testing)
- ✅ HTTPS/WSS encryption (via Railway and hosting platform)
- ❌ No authentication on signaling server
- ❌ No rate limiting
- ❌ No CORS restrictions
- ❌ No API keys

### For Production Use
Consider adding:
1. **Authentication**: JWT tokens or API keys
2. **Rate Limiting**: Prevent abuse
3. **CORS**: Restrict to your domain
4. **TURN Servers**: For better NAT traversal
5. **Monitoring**: Track usage and errors
6. **Managed Service**: Consider Twilio/PubNub for production

## Scaling Considerations

**Current Architecture:**
- Signaling server handles ~1000s of connections
- P2P means no bandwidth cost for media
- Railway free tier sufficient for testing
- GitLab Pages handles static files efficiently

**If Scaling Up:**
- Add Redis for multi-instance signaling
- Use professional TURN servers (Twilio, Xirsys)
- Add load balancer for signaling servers
- Consider dedicated WebRTC infrastructure

## Testing Locally vs Production

### Local Development
```bash
# Terminal 1: Start web server
npm run web  # or python3 -m http.server 8000

# Terminal 2: Start signaling server
npm run signaling  # or node webrtc-signaling-server.js

# Access at: http://localhost:8000
```

Configuration:
```javascript
window.SIGNALING_SERVER_URL = 'ws://localhost:8888';
```

### Production
Frontend: `https://username.gitlab.io/the-mirrors-echo/`
Backend: `wss://your-app-name.up.railway.app`

Configuration:
```javascript
window.SIGNALING_SERVER_URL = 'wss://your-app-name.up.railway.app';
```

## Troubleshooting

### Frontend Can't Connect to Backend
- Check `config.js` has correct URL
- Verify using `wss://` not `ws://` or `https://`
- Check Railway deployment is running
- Check browser console for errors

### Video Not Working
- Ensure HTTPS (required for camera access)
- Grant camera permissions
- Check if behind firewall/VPN
- May need TURN servers for some networks

### Railway Deployment Fails
- Check Railway build logs
- Verify `package.json` has `ws` dependency
- Ensure Node.js version >= 16.0.0
- Check `railway.json` configuration

## Cost Estimates

### Free Tier Usage
- **Railway**: $5/month credit (sufficient for signaling)
- **GitLab Pages**: Free unlimited
- **Vercel**: Free for personal projects
- **Netlify**: Free for personal projects

### Estimated Costs
- **Signaling Server**: ~$0-5/month (within free tier)
- **Frontend Hosting**: $0 (static files)
- **Total**: ~$0-5/month for personal use

### If Scaling to 1000s of Users
- May need Railway Pro ($20/month)
- Consider managed WebRTC service
- Add CDN for frontend assets

## Next Steps

1. **Deploy Backend**: Follow [NEXT-STEPS.md](NEXT-STEPS.md)
2. **Deploy Frontend**: Choose hosting platform
3. **Update Config**: Set Railway URL in `config.js`
4. **Test**: Verify end-to-end functionality
5. **Share**: Give URL to others!

## Resources

- **Railway Docs**: https://docs.railway.app
- **WebRTC Docs**: https://webrtc.org/getting-started/overview
- **GitLab CI/CD**: https://docs.gitlab.com/ee/ci/
- **STUN/TURN**: https://www.twilio.com/docs/stun-turn

---

**Architecture Type**: Hybrid (Static Frontend + Serverless Backend + P2P Media)
**Complexity**: Low-Medium
**Cost**: Free to $5/month
**Scalability**: Good (P2P architecture)
