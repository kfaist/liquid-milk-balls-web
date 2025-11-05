# Complete TouchDesigner + LiveKit Return Path Setup

## Overview

This guide explains how to set up the complete bidirectional loop: Remote Camera → LiveKit → TouchDesigner → LiveKit → Remote Viewer.

## Architecture

```
┌─────────────────┐
│ Remote User     │
│ (publisher.html)│
└────────┬────────┘
         │ WebRTC
         ↓
┌─────────────────────┐
│ LiveKit Cloud       │
│ Room: "claymation-  │
│        live"        │
└────────┬────────────┘
         │
         ↓
┌─────────────────────┐
│ OBS Browser Source  │
│ Shows viewer page   │
└────────┬────────────┘
         │ NDI Output
         ↓
┌─────────────────────┐
│ TouchDesigner       │
│ NDI In TOP          │
│ [Your Processing]   │
│ NDI Out TOP         │
└────────┬────────────┘
         │ NDI
         ↓
┌─────────────────────┐
│ OBS NDI Source      │
│ Captures TD output  │
└────────┬────────────┘
         │ WHIP Plugin
         ↓
┌─────────────────────┐
│ LiveKit Cloud       │
│ Room: "processed-   │
│        output"      │
└────────┬────────────┘
         │ WebRTC
         ↓
┌─────────────────────┐
│ Remote User         │
│ (return-viewer.html)│
└─────────────────────┘
```

## Prerequisites

1. **LiveKit Cloud Account**
   - Sign up at https://cloud.livekit.io
   - Create a new project
   - Get your credentials: API Key, API Secret, WebSocket URL

2. **Software Installed**
   - Node.js 18+ (for server)
   - OBS Studio
   - obs-ndi plugin (https://github.com/obs-ndi/obs-ndi)
   - NDI Runtime (https://ndi.video/for-developers/ndi-sdk/download/)
   - TouchDesigner
   - OBS WHIP plugin (for return path)

## Step-by-Step Setup

### Part 1: Server Configuration (5 minutes)

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set environment variables:**

   **On Railway/Production:**
   - Go to your Railway project → Variables
   - Add these variables:
     ```
     LIVEKIT_API_KEY=your_api_key_here
     LIVEKIT_API_SECRET=your_api_secret_here
     LIVEKIT_URL=wss://your-project.livekit.cloud
     ```

   **On Local Development:**
   ```bash
   # Linux/Mac
   export LIVEKIT_API_KEY="your_api_key_here"
   export LIVEKIT_API_SECRET="your_api_secret_here"
   export LIVEKIT_URL="wss://your-project.livekit.cloud"

   # Windows PowerShell
   $env:LIVEKIT_API_KEY="your_api_key_here"
   $env:LIVEKIT_API_SECRET="your_api_secret_here"
   $env:LIVEKIT_URL="wss://your-project.livekit.cloud"
   ```

3. **Start the server:**
   ```bash
   npm start
   ```

   You should see:
   ```
   ✅ Server running on port 3000
   🎥 LiveKit configured:
      Input room: claymation-live
      Processed room: processed-output
   ```

### Part 2: Input Path - Remote Camera → TouchDesigner (10 minutes)

1. **Remote User: Publish Camera**
   - Remote user opens: `https://your-server.com/publisher.html`
   - Click "Start Publishing"
   - Grant camera permissions
   - Their camera is now streaming to LiveKit room "claymation-live"

2. **In OBS: Capture LiveKit Stream**
   - Open OBS Studio
   - Add Source → **Browser Source**
   - Name: "LiveKit Input"
   - URL: `https://your-server.com/viewer.html` (or use ndi-viewer.html if it exists)
   - Width: 1920, Height: 1080
   - Check "Shutdown source when not visible" ✗ (unchecked)
   - Click OK

3. **In OBS: Enable NDI Output**
   - Tools → **NDI™ Output Settings**
   - Check **"Main Output"**
   - Output Name: "OBS" (or any name you want)
   - Click OK

4. **In TouchDesigner: Receive Stream**
   - Add **NDI In TOP** operator
   - In parameters:
     - **Network Source**: Select "OBS (Output)"
     - **Active**: ✓ ON
   - You should now see the remote camera in TouchDesigner!

### Part 3: Output Path - TouchDesigner → Remote Viewer (15 minutes)

#### Step 3A: TouchDesigner → OBS

1. **In TouchDesigner: Send Processed Video**
   - Add **NDI Out TOP** operator after your final processing
   - Connect your output to it
   - In parameters:
     - **Active**: ✓ ON
     - **NDI Name**: "TD-Processed"
     - **Resolution**: Match your output (e.g., 1920x1080)
     - **FPS**: Match your project FPS (e.g., 30 or 60)

2. **In OBS: Receive TouchDesigner Output**
   - Add Source → **NDI™ Source**
   - Name: "TouchDesigner Processed"
   - In source settings:
     - **Source Name**: Select "YOUR-COMPUTER (TD-Processed)"
     - **Bandwidth**: Highest
   - Click OK
   - Your processed video is now in OBS!

#### Step 3B: Install OBS WHIP Plugin

1. **Download OBS WHIP Plugin**
   - Go to: https://github.com/obsproject/obs-websocket/releases (or OBS WHIP plugin repo)
   - Download the latest release for your OS
   - Install the plugin

2. **Restart OBS** after installation

#### Step 3C: Configure OBS to Publish via WHIP

1. **Get WHIP URL from your server:**
   - Open in browser: `http://localhost:3000/api/processed-publisher-token`
   - Copy the `whipUrl` value

   Example response:
   ```json
   {
     "token": "eyJhbGc...",
     "url": "wss://your-project.livekit.cloud",
     "room": "processed-output",
     "whipUrl": "https://your-project.livekit.cloud/whip?access_token=eyJhbGc..."
   }
   ```

2. **In OBS:**
   - Go to **Settings → Stream**
   - Service: Select **"WHIP"**
   - Server: Paste the `whipUrl` you copied
   - Bearer Token: Leave empty (token is in URL)
   - Click **Apply** then **OK**

3. **Start Streaming:**
   - Click **"Start Streaming"** in OBS
   - OBS is now publishing your processed video to LiveKit room "processed-output"!

#### Step 3D: Remote User Views Processed Video

1. **Remote user opens:**
   ```
   https://your-server.com/return-viewer.html
   ```

2. **Click "Join Stream"**
   - They should see your processed TouchDesigner output!
   - They can click "Fullscreen" for immersive viewing

## Testing the Complete Loop

### Quick Test Checklist:

1. ✅ Remote user opens publisher.html → sees their camera
2. ✅ Remote user clicks "Start Publishing" → status shows "Connected"
3. ✅ OBS Browser Source shows remote camera feed
4. ✅ TouchDesigner NDI In TOP shows remote camera
5. ✅ TouchDesigner processing is visible in your network
6. ✅ OBS NDI Source shows TouchDesigner processed output
7. ✅ OBS is streaming (bottom status bar shows "Live")
8. ✅ Remote user opens return-viewer.html → clicks "Join Stream"
9. ✅ Remote user sees processed video!

## Troubleshooting

### "LiveKit not configured" error

**Problem:** Server can't generate tokens

**Solution:**
- Verify environment variables are set correctly
- Restart the server after setting variables
- Check LiveKit credentials are valid

### OBS Browser Source is black/empty

**Problem:** Viewer page not loading

**Solution:**
- Check server is running
- Verify URL is correct
- Try refreshing the browser source (right-click → Refresh)
- Check browser console for errors

### TouchDesigner doesn't see NDI source

**Problem:** NDI In TOP shows no sources

**Solution:**
- Ensure NDI Runtime is installed
- Restart TouchDesigner after enabling OBS NDI Output
- Both OBS and TouchDesigner must run with same permissions (both admin or both regular user)
- Check Windows Firewall isn't blocking NDI

### OBS doesn't see TouchDesigner NDI Out

**Problem:** NDI Source list doesn't show TD-Processed

**Solution:**
- Verify NDI Out TOP is **Active** (checkbox on)
- Restart OBS after starting TouchDesigner NDI Out
- Check both apps have same privilege level
- Try a different NDI Name

### OBS WHIP streaming fails

**Problem:** "Failed to connect" or "Invalid token" errors

**Solution:**
- Verify WHIP URL is complete and includes access_token
- Check LiveKit credentials are correct
- Ensure token hasn't expired (regenerate from /api/processed-publisher-token)
- Try restarting OBS

### Return viewer shows black screen

**Problem:** return-viewer.html connects but no video

**Solution:**
- Verify OBS is actively streaming (check "Live" indicator)
- Check OBS scene has the TouchDesigner source visible and not hidden
- Refresh return-viewer.html page
- Check browser console for WebRTC errors
- Verify you're using the correct room (processed-output)

## API Endpoints Reference

### `/api/publisher-token`
- **Purpose:** Remote camera publishing to input room
- **Room:** claymation-live
- **Permissions:** Publish + Subscribe

### `/api/viewer-token`
- **Purpose:** Viewing input room (for OBS Browser Source)
- **Room:** claymation-live
- **Permissions:** Subscribe only

### `/api/processed-publisher-token`
- **Purpose:** OBS WHIP publishing processed video
- **Room:** processed-output
- **Permissions:** Publish only
- **Returns:** `whipUrl` for OBS WHIP configuration

### `/api/processed-viewer-token`
- **Purpose:** Remote users viewing processed video
- **Room:** processed-output
- **Permissions:** Subscribe only

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LIVEKIT_API_KEY` | LiveKit API Key | `APISomething123` |
| `LIVEKIT_API_SECRET` | LiveKit API Secret | `SecretKey456...` |
| `LIVEKIT_URL` | LiveKit WebSocket URL | `wss://your-project.livekit.cloud` |
| `LIVEKIT_ROOM_NAME` | Input room name (optional) | `claymation-live` (default) |
| `LIVEKIT_PROCESSED_ROOM` | Processed room name (optional) | `processed-output` (default) |

## Production Deployment

### On Railway:

1. **Push your code to GitHub**
2. **Connect Railway to your repository**
3. **Add environment variables** in Railway dashboard
4. **Deploy**

Railway will automatically:
- Install dependencies (`npm install`)
- Start the server (`npm start`)
- Provide HTTPS URLs for all pages

### URLs will be:
- Publisher: `https://your-app.up.railway.app/publisher.html`
- Return Viewer: `https://your-app.up.railway.app/return-viewer.html`

## Summary

You now have a complete bidirectional loop:

1. **Remote camera** → LiveKit input room → OBS → NDI → TouchDesigner
2. **TouchDesigner** → NDI → OBS → WHIP → LiveKit processed room → Remote viewer

This provides:
- ✅ Browser-native (no apps needed for remote users)
- ✅ Low latency (sub-second with LiveKit)
- ✅ Production-ready (scalable to many viewers)
- ✅ Real-time processing visible to remote users
- ✅ Works across any network (no port forwarding needed)

Perfect for:
- Remote collaborations
- Live performances with processing
- Interactive installations with remote participants
- Art shows where viewers see processed versions of their cameras
