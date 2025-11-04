# Copilot Instructions for liquid-milk-balls-web

## Project Overview

**The Mirror's Echo** is an interactive web experience and WebRTC camera streaming system designed for artistic installations. It enables streaming from remote cameras through OBS to TouchDesigner for live projection displays.

**Key Technologies:**
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Backend:** Node.js with Express
- **Real-time Communication:** WebRTC (peer-to-peer) and WebSocket signaling
- **Optional Integration:** LiveKit for production streaming
- **Deployment Targets:** GitLab Pages (static), Railway (server), Vercel/Netlify

## Repository Structure

```
liquid-milk-balls-web/
├── index.html                  # Main page with interactive mirror and WebRTC
├── ndi-viewer.html            # LiveKit viewer page
├── viewer.html                 # Alternative viewer
├── styles.css                  # All styling with glassmorphism effects
├── script.js                   # Mirror interaction logic
├── webrtc-client.js           # Custom WebRTC peer-to-peer client (PRIMARY)
├── server.js                   # Express + WebSocket signaling server
├── webrtc-signaling-server.js # Legacy standalone signaling server
├── config.js                   # WebSocket URL auto-configuration
├── client/
│   └── livekit-join.js        # LiveKit client implementation
├── server/
│   ├── api/                   # Server API endpoints
│   └── README-LIVEKIT.md      # LiveKit server documentation
└── docs/                       # Additional documentation
```

## Development Workflow

### Prerequisites
- **Node.js:** >= 18.0.0 (check with `node --version`)
- **npm:** >= 7.0.0 (check with `npm --version`)

### Setup
```bash
# Install dependencies
npm install

# Start development server (includes HTTP + WebSocket signaling)
npm start

# Validate environment
npm run validate
```

### Testing
- **No automated test suite exists** - manual testing is required
- Test WebRTC locally by opening multiple browser tabs at `http://localhost:3000`
- Test signaling server WebSocket connection at `ws://localhost:3000/ws`
- For LiveKit features, ensure environment variables are set

### Building
- **No build step required** - this is a static site with vanilla JavaScript
- The `.gitlab-ci.yml` handles deployment by copying files to `public/` directory

### Running the Application
```bash
# Development mode
npm start  # Starts on http://localhost:3000

# Access the application
- Main app: http://localhost:3000
- LiveKit viewer: http://localhost:3000/ndi-viewer.html
```

## Code Style and Conventions

### JavaScript
- Use vanilla JavaScript (ES6+) - no frameworks
- Prefer `const` over `let`, avoid `var`
- Use descriptive variable names (e.g., `echoMessages` not `msgs`)
- Add comments for complex WebRTC logic and WebSocket message handling
- Handle errors gracefully with try-catch blocks, especially for WebRTC operations

### HTML/CSS
- Use semantic HTML5 elements
- Maintain the existing glassmorphism design aesthetic
- Responsive design is essential - test on mobile devices
- CSS animations should be smooth (use `transition` and `transform`)

### WebRTC Specifics
- **Primary Implementation:** Use `webrtc-client.js` for peer-to-peer WebRTC
- **LiveKit:** Only use for production/scalable streaming scenarios
- Always check for browser compatibility (getUserMedia, RTCPeerConnection)
- Include fallbacks and error messages for unsupported browsers
- Test camera permissions carefully

### Server Code
- Express routes should be clearly documented
- WebSocket messages should be logged for debugging
- Environment variables should have sensible defaults
- Port should default to 3000 but respect `PORT` environment variable

## Important Context

### WebRTC Architecture
The project supports **two WebRTC modes**:

1. **Simple WebRTC (webrtc-client.js)** - DEFAULT
   - Peer-to-peer with custom WebSocket signaling
   - Free, no external services required
   - Uses Google's public STUN server
   - Best for: Local testing, simple peer connections
   - Signaling endpoint: `/ws` on the same server

2. **LiveKit (client/livekit-join.js)** - OPTIONAL
   - Production-ready with built-in TURN servers
   - Requires API credentials (LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL)
   - Scalable to multiple participants
   - Best for: Production deployments, NDI streaming

**Important:** When modifying `index.html`, ensure it's using the correct WebRTC implementation. The project was previously using LiveKit but reverted to custom WebRTC due to CDN loading issues.

### Environment Variables
```bash
# For LiveKit features only
LIVEKIT_API_KEY="your-api-key"
LIVEKIT_API_SECRET="your-api-secret"
LIVEKIT_URL="wss://your-project.livekit.cloud"
LIVEKIT_ROOM_NAME="claymation-live"  # Optional, defaults to 'claymation-live'

# Server configuration
PORT=3000  # Optional, defaults to 3000
```

### Deployment Notes

#### GitLab Pages (Static Site)
- Configured in `.gitlab-ci.yml`
- Deploys from `main` or `master` branch
- Only includes static files (HTML, CSS, JS)
- URL: `https://kfaist.gitlab.io/the-mirrors-echo/`

#### Railway (Full Application)
- Deploys the full Node.js server
- Supports WebSocket connections over WSS
- Auto-assigns PORT environment variable
- Include `railway.json` for configuration

#### Browser Caching
- Users may experience caching issues after deployment
- Always test with hard refresh (Ctrl+Shift+R)
- Consider cache-busting strategies for production

## Common Tasks

### Adding New Features to the Mirror Interaction
1. Edit `script.js` to add interaction logic
2. Update `styles.css` for visual effects
3. Test in multiple browsers (Chrome, Firefox, Safari)
4. Ensure mobile responsiveness

### Modifying WebRTC Functionality
1. Edit `webrtc-client.js` for peer-to-peer changes
2. Update `server.js` if signaling logic needs changes
3. Test with multiple browser tabs/devices
4. Check browser console for WebRTC errors
5. Verify STUN/TURN server configuration

### Updating LiveKit Integration
1. Edit `client/livekit-join.js` for client changes
2. Update `server/api/` for server-side changes
3. Ensure environment variables are set
4. Test with LiveKit dashboard

### Deployment Changes
1. For static deployment: Update `.gitlab-ci.yml`
2. For Railway: Update `railway.json` and check `server.js`
3. Always test locally first: `npm start`
4. Document any new environment variables needed

## Security Considerations

- **Never commit secrets** - use environment variables
- The simple WebRTC signaling server is **not production-secure** - it relays all messages to all clients
- For production, use LiveKit or implement proper authentication
- Enable HTTPS/WSS for production deployments
- Validate user inputs, especially in WebSocket message handlers
- Consider rate limiting for production deployments

## Troubleshooting

### Common Issues

**"npm is not recognized"**
- Node.js not installed or not in PATH
- Restart terminal after installation

**"Cannot find module 'express'"**
- Run `npm install` in the project directory

**"Port 3000 already in use"**
- Another process is using port 3000
- Kill the process or use: `PORT=3001 npm start`

**WebRTC connection fails**
- Check browser console for errors
- Verify WebSocket connection to `/ws`
- Ensure camera permissions are granted
- Try with two different browsers/devices

**"LiveKit SDK not loaded"**
- Browser cache issue - hard refresh (Ctrl+Shift+R)
- Verify correct script tag in HTML
- Check CDN availability

**NDI not working in OBS/TouchDesigner**
- Ensure NDI Runtime is installed
- Enable NDI Output in OBS (Tools → NDI Output Settings)
- Check that OBS is outputting to NDI

## Documentation

- `README.md` - Main project documentation
- `WEBRTC-SETUP.md` - Complete WebRTC and NDI/OBS integration guide
- `RAILWAY.md` - Railway deployment guide
- `RAILWAY-TROUBLESHOOTING.md` - Deployment issue resolution
- `LIVEKIT-SETUP-GUIDE.md` - LiveKit configuration guide
- `HANDOFF-PROMPT.md` - Project context and technical details
- `CONTRIBUTING.md` - Contribution guidelines (currently minimal)

## User Context

The primary user (Krista) is a VR/AI artist who:
- Uses this for live projection installations
- Prefers clear, step-by-step instructions
- Works with OBS and TouchDesigner
- May have dyslexia - needs actionable guidance

When providing instructions:
- Be clear and direct
- Use numbered steps
- Provide exact commands to run
- Include expected outcomes
- Offer troubleshooting tips

## License

**GNU AGPL-3.0-or-later** - This is a copyleft license
- Any modifications must also be open-sourced under AGPL
- Commercial licensing available - contact kristabluedoor@gmail.com
- See `LICENSE` and `LICENSE-INFO.md` for details

## Guidelines for Making Changes

1. **Understand the WebRTC mode** - Check which implementation (custom vs LiveKit) is active
2. **Test locally** - Always run `npm start` and test before committing
3. **Consider caching** - Users may have cached versions, document cache-clearing steps
4. **Mobile-first** - Test on mobile devices, especially for camera access
5. **Document changes** - Update relevant .md files if changing functionality
6. **Minimal dependencies** - Prefer vanilla JavaScript over adding new libraries
7. **Respect the aesthetic** - Maintain the glassmorphism design language
8. **Check all deployment targets** - Changes may affect GitLab Pages, Railway, etc.
9. **No tests to update** - Manual testing only; be thorough
10. **OBS/TouchDesigner compatibility** - Test NDI integration if changing video/canvas elements
