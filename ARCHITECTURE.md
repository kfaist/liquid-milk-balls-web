# Architecture Overview

## System Flow

This document explains how the webcam streaming system works from browser to TouchDesigner and back.

## Pages and Their Purposes

### 1. **publisher.html** (NEW)
- **Purpose**: Publish webcam from any browser/network to LiveKit
- **Technology**: LiveKit Client SDK
- **User**: Remote user or anyone who wants to stream their camera
- **Flow**: Camera → LiveKit Room

### 2. **ndi-viewer.html**
- **Purpose**: View LiveKit stream (designed to be captured by OBS)
- **Technology**: LiveKit Client SDK (viewer mode)
- **User**: Captured by OBS Browser Source
- **Flow**: LiveKit Room → Video Display

### 3. **index.html**
- **Purpose**: Main landing page with demo and links
- **Technology**: Simple peer-to-peer WebRTC (for testing only)
- **User**: Entry point, showcases the project
- **Flow**: Provides navigation to publisher and viewer pages

### 4. **viewer.html**
- **Purpose**: Auto-connecting P2P viewer (legacy/testing)
- **Technology**: Simple WebRTC peer-to-peer
- **User**: For local testing without LiveKit
- **Flow**: P2P WebRTC connection

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         REMOTE USER (Any Network)                   │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  publisher.html                                            │    │
│  │  - Opens in browser                                        │    │
│  │  - Clicks "Start Publishing"                               │    │
│  │  - Webcam captured via getUserMedia                        │    │
│  └──────────────────┬─────────────────────────────────────────┘    │
└─────────────────────┼──────────────────────────────────────────────┘
                      │
                      │ WebRTC (LiveKit)
                      ▼
            ┌──────────────────┐
            │  LiveKit Cloud   │
            │  or Self-Hosted  │
            │  Room: "xxx"     │
            └────────┬─────────┘
                     │
                     │ WebRTC (LiveKit)
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      YOUR COMPUTER (Local)                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  OBS Studio                                                │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │  Browser Source: ndi-viewer.html                 │     │    │
│  │  │  - Auto-connects to LiveKit                      │     │    │
│  │  │  - Displays remote webcam                        │     │    │
│  │  └────────────────┬─────────────────────────────────┘     │    │
│  │                   │                                        │    │
│  │                   │ NDI Output Enabled                     │    │
│  └───────────────────┼────────────────────────────────────────┘    │
│                      │                                              │
│                      │ NDI Protocol (local network)                │
│                      ▼                                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  TouchDesigner                                             │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │  NDI In TOP                                      │     │    │
│  │  │  - Receives from OBS NDI                         │     │    │
│  │  │  - Process video (effects, compositing, etc.)    │     │    │
│  │  │  ↓                                               │     │    │
│  │  │  NDI Out TOP                                     │     │    │
│  │  │  - Sends processed video back to OBS             │     │    │
│  │  └──────────────┬───────────────────────────────────┘     │    │
│  └─────────────────┼────────────────────────────────────────┘    │
│                    │ NDI (back to OBS)                           │
│                    ▼                                             │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  OBS Studio (Receive Processed Video)                     │    │
│  │  - NDI Source: "TouchDesigner-Processed"                  │    │
│  │  - Options:                                                │    │
│  │    • Virtual Camera (for video apps)                      │    │
│  │    • Publish to second LiveKit room                       │    │
│  │    • RTMP streaming (YouTube, Mux, etc.)                  │    │
│  └────────────────┬───────────────────────────────────────────┘    │
└───────────────────┼──────────────────────────────────────────────┘
                    │
                    │ (Via Virtual Camera, LiveKit, or RTMP)
                    ▼
          [Return Viewer Page or Video App]
                    │
                    ▼
           Remote User sees processed video
```

## Technology Stack

### LiveKit (Production)
- **Used by**: publisher.html, ndi-viewer.html
- **Purpose**: Scalable WebRTC streaming
- **Advantages**: 
  - Works across any network (NAT traversal built-in)
  - Supports multiple viewers
  - Production-ready infrastructure
  - No firewall/router configuration needed

### Simple WebRTC (Testing)
- **Used by**: index.html (webrtc-client.js), viewer.html
- **Purpose**: Local testing and development
- **Advantages**: 
  - No external service needed
  - Direct peer-to-peer connection
  - Good for understanding WebRTC basics
- **Limitations**: 
  - Only works on local network or with TURN servers
  - Limited to 2 peers
  - Not production-ready

## Server Endpoints

### WebSocket
- **Path**: `/ws`
- **Purpose**: Signaling for simple P2P WebRTC
- **Used by**: webrtc-client.js, viewer.html

### LiveKit Token APIs
- **Path**: `/api/publisher-token`
  - **Purpose**: Generate token for publishing to LiveKit
  - **Used by**: publisher.html
  
- **Path**: `/api/viewer-token`
  - **Purpose**: Generate token for viewing LiveKit stream
  - **Used by**: ndi-viewer.html

## Configuration

### Environment Variables (Required for LiveKit)
```bash
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_ROOM_NAME=claymation-live  # Optional, defaults to this
```

### Without LiveKit
If LiveKit is not configured:
- publisher.html will show an error
- ndi-viewer.html will show an error
- index.html simple WebRTC still works for local testing

## Use Cases

### Use Case 1: Remote Performer to TouchDesigner
**Scenario**: A performer at home wants to stream to your TouchDesigner installation

**Steps**:
1. Send performer link to `https://your-server.com/publisher.html`
2. Performer clicks "Start Publishing"
3. In OBS, add Browser Source: `https://your-server.com/ndi-viewer.html`
4. Enable NDI output in OBS
5. In TouchDesigner, add NDI In TOP
6. Process and display

### Use Case 2: Local Testing
**Scenario**: Test WebRTC without LiveKit credentials

**Steps**:
1. Open `http://localhost:3000/` in browser 1
2. Click "Start Camera" → "Start WebRTC Call"
3. Open `http://localhost:3000/viewer.html` in browser 2
4. See the P2P connection work
5. Capture browser 2 in OBS for NDI output

### Use Case 3: Installation with Multiple Cameras
**Scenario**: Multiple remote cameras feeding into one TouchDesigner instance

**Steps**:
1. Each camera opens `publisher.html` on their device
2. All publish to the same LiveKit room
3. Open multiple `ndi-viewer.html` instances in OBS (each as a separate source)
4. Each NDI source goes to TouchDesigner
5. Composite all feeds in TouchDesigner

### Use Case 4: Complete Bidirectional Loop
**Scenario**: Remote user sees their camera processed through TouchDesigner in real-time

**Steps (Input Path)**:
1. Remote user opens `publisher.html` and publishes camera
2. Open `ndi-viewer.html` in OBS Browser Source
3. Enable OBS NDI Output (Tools → NDI Output Settings)
4. In TouchDesigner, add NDI In TOP and select OBS source
5. Process the video in your TouchDesigner network

**Steps (Output Path)**:
6. Add NDI Out TOP after your processing chain in TouchDesigner
7. Set NDI Out TOP to Active with a unique name (e.g., "TD-Processed")
8. In OBS, add NDI™ Source and select your TouchDesigner NDI Out
9. Use one of these methods to send back:
   - **Option A:** Start OBS Virtual Camera, share in video app
   - **Option B:** Set up second LiveKit room for processed video
   - **Option C:** Stream via RTMP to YouTube Live, Mux, etc.
   - **Option D:** Use screen/window capture of OBS output

See **[TOUCHDESIGNER-OUTPUT-GUIDE.md](TOUCHDESIGNER-OUTPUT-GUIDE.md)** for detailed instructions.

## Troubleshooting Guide

### "LiveKit not configured" Warning
- Set environment variables for LiveKit
- Restart the server after setting variables
- Use simple WebRTC mode for local testing instead

### Camera Not Accessible
- Must use `https://` or `http://localhost`
- Grant camera permissions in browser
- Check if another app is using the camera

### No Video in OBS
- Ensure ndi-viewer.html is in the Browser Source URL
- Check that publisher is actively streaming
- Refresh the Browser Source in OBS
- Check browser console for errors

### NDI Not Showing in TouchDesigner
- Verify NDI Runtime is installed
- Check OBS → Tools → NDI Output Settings is enabled
- Ensure both OBS and TouchDesigner are on same network
- Restart TouchDesigner if needed

## Security Notes

- Simple WebRTC signaling server is **not secure** - for testing only
- LiveKit tokens expire after 2 hours (configurable in server.js)
- Always use HTTPS in production
- Consider authentication for publisher page in production
