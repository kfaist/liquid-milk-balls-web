# COORDINATION INFO FOR OTHER AGENT

## Current Project Status - TouchDesigner WebRender TOP Integration

**What I'm Building:**
- TouchDesigner integration with LiveKit for receiving remote browser camera feeds
- Files/Components:
  - `ndi-streamCOPY.toe` - TouchDesigner project with WebRender TOP
  - `/webrender_livekit_input` - WebRender TOP operator for receiving browser streams
  - `td-auto-viewer.html` - LiveKit viewer page that WebRender loads
  - Node.js server on localhost:3000 serving the viewer pages

**Current Status:**
✅ OUTPUT Pipeline 100% WORKING:
- TouchDesigner → NDI → OBS Studio → WHIP → LiveKit Cloud → Global Viewers
- Processed video successfully streams to viewers worldwide

⚠️ INPUT Pipeline (What I'm Currently Fixing):
- Browser Cameras → LiveKit → TouchDesigner WebRender TOP
- WebRender TOP exists but needs URL configuration
- Should load: http://localhost:3000/td-auto-viewer.html
- Currently shows yellow warning triangle (being debugged)

**Timeline:**
- INPUT fix: ~5-15 minutes (just parameter configuration)
- Full bidirectional flow should be working very soon

**Current Blocker:**
- WebRender TOP URL parameter needs to be set correctly
- Currently working on getting it to load td-auto-viewer.html properly

---

## LiveKit Configuration (SHARED CREDENTIALS)

**LiveKit Cloud Details:**
```
URL: wss://claymation-transcription-l6e51sws.livekit.cloud
API Key: APITw2Yp2Tv3yfg
API Secret: eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
```

**Room Names:**
```
Input Room: claymation-live
(This is where browser cameras publish to)

Output Room: processed-output
(This is where TouchDesigner sends processed video)
```

**Authentication Method:**
- Using LiveKit JWT tokens generated server-side
- Node.js server generates tokens using LiveKit Server SDK
- Tokens include room name and participant permissions

---

## File Ownership (Proposed)

**You Own (Other Agent):**
- `main-site.html` - Hybrid dual-stream container with visual effects
- Custom viewer pages with shimmer/raindrop effects
- Visual effects timing and polish

**I Own (This Agent):**
- `publisher.html` - Browser camera publishing interface
- `td-auto-viewer.html` - LiveKit viewer for TouchDesigner WebRender
- `return-viewer.html` - Global viewer for processed output
- TouchDesigner project and NDI/OBS pipeline
- Node.js server (server.js)

**Shared:**
- LiveKit Cloud credentials (same for both)
- Railway deployment configuration
- `.env` file with credentials

---

## Integration Points

**For Your main-site.html:**

**1. Local Camera → Publish to LiveKit:**
```javascript
// Use these exact credentials
const livekitUrl = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const roomName = 'claymation-live';

// Get token from server
const response = await fetch('/api/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    roomName: 'claymation-live',
    participantName: 'main-site-publisher'
  })
});
const { token } = await response.json();

// Connect and publish
const room = new LivekitClient.Room();
await room.connect(livekitUrl, token);

// Publish local camera
const localTrack = await LivekitClient.createLocalVideoTrack();
await room.localParticipant.publishTrack(localTrack);
```

**2. Remote Stream → Subscribe from LiveKit:**
```javascript
// Subscribe to processed output room
const outputRoomName = 'processed-output';

// Get token for output room
const tokenResponse = await fetch('/api/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    roomName: 'processed-output',
    participantName: 'main-site-viewer'
  })
});
const { token: outputToken } = await tokenResponse.json();

// Connect to output room
const outputRoom = new LivekitClient.Room();
await outputRoom.connect(livekitUrl, outputToken);

// Handle incoming tracks
outputRoom.on('trackSubscribed', (track) => {
  if (track.kind === 'video') {
    const videoElement = document.getElementById('processed-video');
    track.attach(videoElement);
  }
});
```

---

## Server Endpoints Available

My Node.js server (localhost:3000) provides:

**GET /publisher.html**
- Browser camera publishing interface

**GET /td-auto-viewer.html**
- LiveKit viewer for TouchDesigner

**GET /return-viewer.html**
- Global viewer for processed output

**POST /api/token**
- Generates LiveKit JWT tokens
- Body: `{ roomName: string, participantName: string }`
- Returns: `{ token: string }`

---

## Quick Sync Answers

**Q: What's the room name you're using?**
A: Two rooms:
- `claymation-live` - For input (browser cameras publish here)
- `processed-output` - For output (TouchDesigner processed video)

**Q: What's the LiveKit URL?**
A: `wss://claymation-transcription-l6e51sws.livekit.cloud`

**Q: What authentication method?**
A: JWT tokens generated server-side
- POST to `/api/token` with room name and participant name
- Server returns token using API key/secret
- Use token to connect to LiveKit room

---

## Update Schedule

**Recommendation:**
- Work in parallel on different files
- You work on `main-site.html` with visual effects
- I work on TouchDesigner WebRender TOP configuration
- Both use the same LiveKit credentials above
- Test integration once both parts are working

**Sync Frequency:**
- Check in when major milestones complete
- I'll notify when WebRender TOP is receiving streams
- You notify when main-site can publish/subscribe
- Final integration test together

---

## Next Steps for Integration

**Once I Fix WebRender TOP (ETA: 15 min):**
1. Browser camera → LiveKit room "claymation-live" ✅
2. TouchDesigner WebRender loads td-auto-viewer.html ⚠️ (fixing now)
3. TouchDesigner processes video ✅
4. Output → NDI → OBS → LiveKit room "processed-output" ✅
5. Your main-site.html subscribes to "processed-output" ⏳ (needs implementation)

**For Your main-site.html:**
1. Implement camera publish to "claymation-live" room
2. Implement subscribe to "processed-output" room
3. Wire up video elements to LiveKit tracks
4. Keep all visual effects (shimmer, raindrops, etc.)

---

## Testing Plan

**Phase 1: Independent Testing**
- You test: Can main-site.html publish camera to LiveKit?
- I test: Can TouchDesigner receive from LiveKit?

**Phase 2: End-to-End Test**
- Open main-site.html
- Verify camera publishes to "claymation-live"
- Verify TouchDesigner receives and processes
- Verify processed output appears in "processed-output"
- Verify main-site.html shows processed video

**Phase 3: Visual Effects Polish**
- Confirm effects work with real video
- Adjust timing/opacity as needed
- Final polish

---

## Contact Info

**Current Session Agent (Me):**
- Working on: TouchDesigner WebRender TOP input configuration
- Status: WebRender TOP exists, needs URL parameter fix
- ETA: 5-15 minutes to complete

**Files Ready to Share:**
- All LiveKit credentials in `.env` file
- Server running on localhost:3000
- publisher.html, td-auto-viewer.html, return-viewer.html all working

**Ready for Integration!** 🚀
