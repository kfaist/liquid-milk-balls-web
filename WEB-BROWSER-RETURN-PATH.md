# Getting Processed Video Back into a Web Browser

## The Question: "How does it get BACK in the web browser the viewer is on though?"

Great question! This guide explains **exactly** how to get your TouchDesigner-processed video back into a web browser for the remote user to view.

## The Missing Link

You have:
- ✅ Remote camera → LiveKit → OBS → TouchDesigner (NDI In TOP) → Processing → TouchDesigner (NDI Out TOP) → OBS (NDI Source)

You need:
- ❓ OBS → **[MISSING STEP]** → Web Browser (return-viewer.html)

## The Solution: 3 Methods

### Method 1: Second LiveKit Room (Recommended for Production)

This is the cleanest solution for getting video back into a web browser.

#### Overview
```
OBS (with processed video) → Publish to LiveKit Room #2 → return-viewer.html displays it
```

#### Step-by-Step

**1. Modify server.js to support a second room:**

Create a new token endpoint for the "processed" room:

```javascript
// Add this to server.js after the existing token endpoints
app.get("/api/processed-publisher-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({
        error: 'LiveKit not configured',
        message: 'Set LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL'
      });
    }
    
    const participantIdentity = `processed-publisher-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '2h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'processed-room', // Different room name
      canSubscribe: true,
      canPublish: true,
    });
    
    const jwt = await token.toJwt();
    console.log(`[processed-publisher-token] Generated for ${participantIdentity}`);
    
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'processed-room',
      identity: participantIdentity
    });
  } catch (error) {
    console.error('[processed-publisher-token] Error:', error);
    res.status(500).json({ error: 'Token generation failed', details: error.message });
  }
});

app.get("/api/processed-viewer-token", async (req, res) => {
  try {
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
      return res.status(500).json({
        error: 'LiveKit not configured',
        message: 'Set LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL'
      });
    }
    
    const participantIdentity = `processed-viewer-${Math.random().toString(36).substring(7)}`;
    const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      ttl: '2h',
    });
    
    token.addGrant({
      roomJoin: true,
      room: 'processed-room', // Same room name as publisher
      canSubscribe: true,
      canPublish: false, // Viewers can't publish
    });
    
    const jwt = await token.toJwt();
    console.log(`[processed-viewer-token] Generated for ${participantIdentity}`);
    
    res.json({
      token: jwt,
      url: LIVEKIT_URL,
      roomName: 'processed-room',
      identity: participantIdentity
    });
  } catch (error) {
    console.error('[processed-viewer-token] Error:', error);
    res.status(500).json({ error: 'Token generation failed', details: error.message });
  }
});
```

**2. Install OBS WHIP Plugin:**

Download from: https://github.com/obsproject/obs-webrtc/releases

This plugin lets OBS publish video to WebRTC servers like LiveKit.

**3. Configure OBS WHIP Output:**

In OBS:
- Go to **Settings → Stream**
- Service: Select **WHIP**
- Server: `https://YOUR-LIVEKIT-URL/rtc/v1/whip`
  - Replace `YOUR-LIVEKIT-URL` with your LiveKit server URL
  - For LiveKit Cloud: `https://YOUR-PROJECT.livekit.cloud/rtc/v1/whip`
- Bearer Token: Get from `/api/processed-publisher-token` endpoint
  - Open browser: `http://localhost:3000/api/processed-publisher-token`
  - Copy the `token` value
  - Paste into Bearer Token field
- Click **OK**

**4. Update return-viewer.html:**

Modify the token endpoint it uses:

```javascript
// In return-viewer.html, find this line:
const response = await fetch('/api/viewer-token');

// Change it to:
const response = await fetch('/api/processed-viewer-token');
```

**5. Start Streaming:**

- In OBS, click **Start Streaming**
- Open `return-viewer.html` in browser
- Click "Connect"
- The processed video from TouchDesigner now appears in the browser!

### Method 2: Use getUserMedia with OBS Virtual Camera (Simpler Setup)

This method uses OBS Virtual Camera as a "fake webcam" that browsers can access.

#### How It Works
```
OBS (with processed video) → Virtual Camera → Browser getUserMedia → Display in HTML
```

#### Step-by-Step

**1. Start OBS Virtual Camera:**
- In OBS: **Tools → Virtual Camera → Start Virtual Camera**

**2. Create a simple viewer page:**

Create `webcam-return-viewer.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Processed Video Viewer</title>
    <style>
        body { margin: 0; background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; }
        video { max-width: 100%; max-height: 100%; }
    </style>
</head>
<body>
    <video id="video" autoplay playsinline></video>
    
    <script>
        async function startCamera() {
            try {
                // Get list of video devices
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                
                // Find OBS Virtual Camera
                const obsCamera = videoDevices.find(device => 
                    device.label.includes('OBS') || device.label.includes('Virtual')
                );
                
                const constraints = {
                    video: {
                        deviceId: obsCamera ? { exact: obsCamera.deviceId } : undefined,
                        width: { ideal: 1920 },
                        height: { ideal: 1080 }
                    },
                    audio: false
                };
                
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                document.getElementById('video').srcObject = stream;
                
            } catch (error) {
                console.error('Error accessing camera:', error);
                alert('Could not access OBS Virtual Camera. Make sure:\n1. OBS Virtual Camera is started\n2. You granted camera permissions\n3. You are using https:// or localhost');
            }
        }
        
        startCamera();
    </script>
</body>
</html>
```

**3. Open in browser:**
- Navigate to `http://localhost:3000/webcam-return-viewer.html`
- Grant camera permissions
- The browser will access OBS Virtual Camera and show the processed video!

**Limitation:** This requires the browser to be on the same computer as OBS, OR you need to share the page via screen sharing.

### Method 3: MediaStream Capture API (Browser-to-Browser)

For a more advanced solution that keeps everything in the browser:

**Concept:**
- Capture OBS output window using `getDisplayMedia()`
- Create a new publisher that sends this capture to LiveKit
- return-viewer.html receives it

This is complex and requires custom code. See Method 1 for a simpler production solution.

## Comparison

| Method | Complexity | Production Ready | Works Remotely | Browser-Only |
|--------|-----------|------------------|----------------|--------------|
| **Method 1: Second LiveKit Room** | Medium | ✅ Yes | ✅ Yes | ✅ Yes |
| **Method 2: OBS Virtual Camera** | Low | ⚠️ Local Only | ❌ No | ✅ Yes |
| **Method 3: Screen Capture** | High | ⚠️ Depends | ✅ Yes | ✅ Yes |

## Recommendation

**For your use case (remote viewer in web browser):**

Use **Method 1: Second LiveKit Room**

**Why?**
- Works across any network (remote users can view from anywhere)
- Browser-native (no apps needed)
- Production-ready
- Maintains the WebRTC architecture you're already using

**Quick summary:**
1. Add two endpoints to server.js for the "processed-room"
2. Install OBS WHIP plugin
3. Configure OBS to stream to LiveKit's WHIP endpoint using a token
4. Update return-viewer.html to use the processed-viewer-token
5. Done! Processed video appears in browser.

## Full Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Remote User #1 (Camera)                     │
│  publisher.html → LiveKit Room "claymation-live"                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  LiveKit Cloud  │
                    │ Room: original  │
                    └────────┬────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Your Computer (Local)                        │
│                                                                 │
│  OBS Browser Source (ndi-viewer.html) ← Subscribes to Room #1  │
│          ↓ (NDI Output)                                        │
│  TouchDesigner (NDI In TOP)                                    │
│          ↓ (Process video)                                     │
│  TouchDesigner (NDI Out TOP)                                   │
│          ↓ (NDI back to OBS)                                   │
│  OBS (NDI Source receives processed video)                     │
│          ↓ (WHIP streaming)                                    │
│  OBS publishes to LiveKit Room "processed-room" ← NEW STEP     │
│                                                                 │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  LiveKit Cloud  │
                    │ Room: processed │
                    └────────┬────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Remote User #2 (Viewer)                      │
│  return-viewer.html → Subscribes to "processed-room"            │
│  Sees the TouchDesigner-processed video in browser! ✅          │
└─────────────────────────────────────────────────────────────────┘
```

## Next Steps

1. Choose Method 1 for production use
2. Add the new endpoints to server.js
3. Install OBS WHIP plugin
4. Test the complete loop locally first
5. Deploy and share return-viewer.html URL with remote users

The key insight: **You need a second LiveKit room** because the first room has the original camera, and the second room has the processed video. They're separate streams in the LiveKit architecture.
