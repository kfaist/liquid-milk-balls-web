# WebRTC Setup Guide

This guide explains how to set up WebRTC for the liquid-milk-balls-web project, including integration with NDI and OBS.

## Prerequisites

Before following this guide, ensure you have **Node.js and npm installed**. If you haven't set up the project yet, please see the [Prerequisites section in the main README](README.md#️-prerequisites) for installation instructions.

## Overview

The project supports **two WebRTC modes**:

1. **Simple WebRTC (Peer-to-Peer)** - For local testing and development
2. **LiveKit** - For production streaming with multiple viewers

## Quick Start - Simple WebRTC

This mode works out of the box without external services.

### 1. Install and Start

**On Windows (PowerShell or Command Prompt):**
```powershell
setup.bat
```

**On macOS/Linux (Terminal):**
```bash
./setup.sh
```

**Or manually (all platforms):**
```bash
npm install
npm start
```

> **Note**: The signaling server is integrated into the main server. The standalone `webrtc-signaling-server.js` is kept for backwards compatibility but is no longer needed.

### 2. Test WebRTC Connection

1. Open `http://localhost:3000` in your browser
2. Click **"Start Camera"** to enable your webcam
3. Click **"Start WebRTC Call"** to connect to the signaling server
4. Open a second browser tab and repeat steps 2-3
5. You should see each other's video feeds

### 3. Integrate with OBS and NDI

To stream from browser to TouchDesigner via OBS:

#### Prerequisites
- **OBS Studio**: [Download here](https://obsproject.com/)
- **obs-ndi plugin**: [Download here](https://github.com/obs-ndi/obs-ndi/releases)
- **NDI Runtime**: [Download here](https://ndi.tv/tools/)

#### Steps

1. **Start your WebRTC session** (steps above)

2. **Capture in OBS**:
   - Open OBS Studio
   - Add a source:
     - **Option A**: Window Capture → Select your browser window
     - **Option B**: Browser Source → Enter `http://localhost:3000`
   - Crop and position as needed

3. **Enable NDI Output in OBS**:
   - Go to **Tools** → **NDI Output Settings**
   - Check **"Main Output"**
   - Give it a name (e.g., "Mirror Echo WebRTC")

4. **Receive in TouchDesigner**:
   - Add an **NDI In TOP** operator
   - Select your OBS NDI source from the dropdown
   - Your WebRTC video stream is now in TouchDesigner!

## Production Setup - LiveKit

For scalable streaming with multiple viewers and production deployments.

### 1. Get LiveKit Credentials

**Option A: LiveKit Cloud (Recommended)**
1. Sign up at [livekit.io](https://livekit.io)
2. Create a new project
3. Get your API Key, API Secret, and WebSocket URL

**Option B: Self-Hosted**
1. Follow the [LiveKit server installation guide](https://docs.livekit.io/oss/deployment/)
2. Configure your self-hosted server
3. Get your API credentials

### 2. Configure Environment Variables

Create a `.env` file (or set environment variables):

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
LIVEKIT_API_KEY="your-api-key-here"
LIVEKIT_API_SECRET="your-api-secret-here"
LIVEKIT_URL="wss://your-project.livekit.cloud"
LIVEKIT_ROOM_NAME="claymation-live"
```

Or export them in your shell:

```bash
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"
export LIVEKIT_URL="wss://your-project.livekit.cloud"
export LIVEKIT_ROOM_NAME="claymation-live"
```

### 3. Start the Server

```bash
npm start
```

You should see:
```
[server] HTTP+WS listening on :3000
[server] LiveKit viewer: /ndi-viewer.html
[server] LiveKit configured for room: claymation-live
```

### 4. Publish to LiveKit

**Option A: Using Browser Publisher Page (Recommended)**
1. Open `http://localhost:3000/publisher.html` in your browser (or share URL with remote user)
2. Click **"Start Publishing"** to stream your webcam to LiveKit
3. Grant camera permissions when prompted
4. Your webcam is now publishing to the LiveKit room

**Option B: Using OBS with LiveKit WHIP**
1. Install [OBS WHIP plugin](https://github.com/obsproject/obs-webrtc)
2. Configure WHIP output with your LiveKit credentials
3. Start streaming to LiveKit room

**Option C: Using LiveKit SDK**
Use the LiveKit client SDK to publish from another application.

### 5. View the Stream

1. Open `http://localhost:3000/ndi-viewer.html` in your browser
2. Click **"Join Live Stream"**
3. The published video stream will appear

### 6. Use with NDI/OBS/TouchDesigner (Complete Loop)

**Complete workflow for remote webcam to TouchDesigner and back:**

1. **Remote User (Publisher)**:
   - Opens `http://your-server:3000/publisher.html` (or Railway URL)
   - Clicks "Start Publishing"
   - Their webcam streams to LiveKit room

2. **Your Computer (OBS)**:
   - Add Browser Source in OBS
   - URL: `http://localhost:3000/ndi-viewer.html` (or your server URL)
   - The viewer automatically connects and shows the remote webcam
   - Go to Tools → NDI Output Settings → Enable "Main Output"

3. **TouchDesigner**:
   - Add NDI In TOP operator
   - Select OBS NDI source from dropdown
   - Process the video as needed
   - Output result back to screen, projector, or another LiveKit room

4. **Return to Browser (Optional)**:
   - TouchDesigner can output processed video back to another web page
   - Use another LiveKit room or simple WebRTC connection
   - Or use Screen Capture to capture TD output window

## Architecture Comparison

### Simple WebRTC (Peer-to-Peer)

```
Browser A ←→ Signaling Server (/ws) ←→ Browser B
          ↓                           ↓
      Direct P2P WebRTC Connection
```

**Pros**:
- No external service required
- Works immediately
- Good for local testing
- Low latency for direct connections

**Cons**:
- Limited to 2 peers
- May fail behind NAT/firewalls
- Not scalable
- No media recording/processing

### LiveKit

```
Publisher → LiveKit Server → Multiple Viewers
                ↓
           Media Routing, Recording, Processing
```

**Pros**:
- Supports multiple publishers/viewers
- Built-in TURN servers
- Media routing and processing
- Production-ready
- Scalable to hundreds of participants
- Recording capabilities

**Cons**:
- Requires LiveKit account or self-hosting
- Additional configuration needed
- Slightly higher latency (due to server routing)

## Troubleshooting

### Simple WebRTC Issues

**"Error: Could not connect to signaling server"**
- Ensure `npm start` is running
- Check that port 3000 is not blocked
- Verify you're accessing `http://localhost:3000` (not a different port)

**"Camera permission denied"**
- Click "Allow" when browser prompts for camera access
- Check browser settings to ensure camera is not blocked
- Use `http://localhost` or `https` (not `file://`)

**"No remote video showing"**
- Ensure both peers have started their cameras
- Check browser console for errors
- Verify both peers are connected to the same signaling server
- Try refreshing both browser tabs

### LiveKit Issues

**"LiveKit not configured" warning**
- Set all required environment variables:
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET`
  - `LIVEKIT_URL`
- Restart the server after setting variables

**"Failed to get token" on ndi-viewer.html**
- Verify your LiveKit credentials are correct
- Check that your API key has permission to create tokens
- Ensure your LiveKit project is active

**"Connection failed" in viewer**
- Verify `LIVEKIT_URL` is correct (should start with `wss://`)
- Check that there's an active publisher in the room
- Ensure firewall allows WebSocket connections

### NDI/OBS Issues

**"NDI source not showing in TouchDesigner"**
- Verify NDI Runtime is installed
- Check that OBS NDI output is enabled
- Ensure both OBS and TouchDesigner are on the same network
- Try restarting OBS after enabling NDI output

**"Poor video quality in NDI stream"**
- Increase video resolution in browser camera constraints (edit `webrtc-client.js`)
- Adjust OBS output resolution
- Check network bandwidth (for remote streaming)

**"NDI stream is laggy"**
- Reduce video resolution
- Check CPU usage (NDI encoding is CPU-intensive)
- Close unnecessary applications
- Use hardware encoding if available in OBS

## Development Tips

### Testing WebRTC Locally

1. Use Chrome/Edge for best WebRTC support
2. Test with multiple browser tabs initially
3. Use different browsers (e.g., Chrome + Firefox) for true peer testing
4. Check browser console for detailed WebRTC logs

### Debugging Connection Issues

Enable verbose WebRTC logging in Chrome:
1. Go to `chrome://webrtc-internals/`
2. Start your WebRTC session
3. View detailed connection statistics and logs

### Customizing Video Constraints

Edit `webrtc-client.js` around line 48:

```javascript
const constraints = {
    video: {
        width: { ideal: 1920 },  // Increase for higher quality
        height: { ideal: 1080 },
        frameRate: { ideal: 30 }
    },
    audio: true
};
```

## Next Steps

- **For local development**: Use Simple WebRTC with the instructions above
- **For production deployment**: Set up LiveKit and deploy to Railway/Heroku/etc.
- **For advanced features**: Explore LiveKit's recording, transcription, and AI features
- **For multiple rooms**: Modify `LIVEKIT_ROOM_NAME` or implement dynamic room creation

## Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [WebRTC API Reference](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- [OBS Studio Documentation](https://obsproject.com/wiki/)
- [NDI Documentation](https://www.ndi.tv/documentation/)
- [TouchDesigner NDI Guide](https://docs.derivative.ca/NDI_In_TOP)
