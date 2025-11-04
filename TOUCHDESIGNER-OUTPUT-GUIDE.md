# TouchDesigner Output Integration Guide

## Overview

This guide explains how to complete the bidirectional loop from remote camera through TouchDesigner and back to the remote viewer.

## Complete Flow Diagram

```
Remote User's Camera
    ↓
[Publisher Page]
    ↓ (WebRTC - LiveKit)
LiveKit Room: "claymation-live"
    ↓
[NDI Viewer Page in OBS Browser Source]
    ↓ (NDI Output from OBS)
TouchDesigner (NDI In TOP)
    ↓ (Your processing/effects)
TouchDesigner (NDI Out TOP) ← YOU ARE HERE
    ↓ (NDI back to OBS)
[OBS - NDI Source]
    ↓ (Virtual Camera or Window Capture)
[Return Viewer Page]
    ↓
Remote User sees processed video
```

## Step-by-Step Setup

### Part 1: Receive Camera Feed (Already Working)

If you've confirmed WebRTC connection, this part is complete:

1. ✅ Remote user opens `publisher.html` and clicks "Start Publishing"
2. ✅ LiveKit receives the video stream
3. ✅ OBS Browser Source shows `ndi-viewer.html`
4. ✅ OBS has NDI Output enabled (Tools → NDI Output Settings → Main Output)
5. ✅ TouchDesigner NDI In TOP receives the stream

### Part 2: Send Processed Video Back to OBS (THIS STEP)

#### Option A: Using NDI Out TOP (Recommended for Live Processing)

1. **In TouchDesigner:**
   - Add an **NDI Out TOP** operator to your network
   - Connect your final processed output to the NDI Out TOP
   - In the NDI Out TOP parameters:
     - **Active**: Enable (turn on)
     - **NDI Name**: Set a name like "TouchDesigner-Processed"
     - **Resolution**: Match your output resolution (e.g., 1920x1080)
     - **FPS**: Match your project FPS (e.g., 30 or 60)

2. **In OBS Studio:**
   - Add a new source: **Sources → Add → NDI™ Source**
   - Give it a name: "TouchDesigner Processed Video"
   - In the NDI™ Source properties:
     - **Source Name**: Select "COMPUTER-NAME (TouchDesigner-Processed)"
     - **Bandwidth**: Select "Highest" for best quality
     - Click **OK**

3. **Verify the connection:**
   - You should now see your processed TouchDesigner output in OBS
   - The video will update in real-time as you modify your TouchDesigner network

#### Option B: Using OBS Window Capture (Simpler but Less Efficient)

If NDI Out is not working or you prefer a simpler method:

1. **In TouchDesigner:**
   - Create a **Window COMP** that shows your final output
   - Set the Window COMP to fullscreen or a specific size
   - Make sure the window is visible on your screen

2. **In OBS Studio:**
   - Add a new source: **Sources → Add → Window Capture**
   - Give it a name: "TouchDesigner Window"
   - In the Window Capture properties:
     - **Window**: Select your TouchDesigner window
     - **Capture Method**: Select "Windows 10 (1903 and up)" if available
     - Click **OK**

### Part 3: Send Back to Remote Viewer

Now that OBS has the processed video, you have several options:

#### Option 1: Use return-viewer.html (Easiest)

**Current Limitation:** The `return-viewer.html` currently connects to the same LiveKit room as the input, so it shows the original camera feed, not the processed video.

**To make this work, you need to create a second publishing path:**

1. **Configure OBS to publish the processed video to LiveKit:**
   - You'll need to use OBS's **Browser Source** with a custom HTML page that publishes to LiveKit
   - OR use OBS WHIP plugin to publish to a different LiveKit room
   - OR use the OBS Virtual Camera and capture it in another browser

2. **For now, the simplest solution is Option 2 below.**

#### Option 2: Use OBS Virtual Camera (Quick Solution)

This is the easiest way to get started:

1. **In OBS Studio:**
   - Make sure your TouchDesigner processed video source is visible in the scene
   - Click **Tools → Virtual Camera → Start Virtual Camera**
   - OBS will create a virtual webcam device

2. **Show to Remote User:**
   - **Option 2a:** Share your screen in Zoom/Discord/etc. and show the OBS preview
   - **Option 2b:** Use another video calling application that can select "OBS Virtual Camera" as the camera source
   - **Option 2c:** Create a custom web page that captures the OBS Virtual Camera (requires getUserMedia)

#### Option 3: Stream via RTMP (Advanced - For Production)

For a production setup where you want remote users to view in a browser:

1. **Set up an RTMP streaming service:**
   - Use services like: Mux, AWS IVS, YouTube Live (unlisted), or Twitch
   - Get your RTMP server URL and stream key

2. **Configure OBS to stream:**
   - **Settings → Stream**
   - Select your service or choose "Custom..."
   - Enter the RTMP server URL and stream key
   - Click **Start Streaming**

3. **Update return-viewer.html:**
   - Modify it to embed an HLS or RTMP video player
   - Point it to your stream's viewing URL
   - Remote users can now view the processed video

#### Option 4: Second LiveKit Room (Best for LiveKit Workflows)

**This requires modifying the server to support a second room:**

1. **Create a new endpoint for "processed video room":**
   ```javascript
   // In server.js, add a new token endpoint
   app.get("/api/processed-token", async (req, res) => {
     // ... similar to viewer-token but for "processed-room"
   });
   ```

2. **In TouchDesigner:**
   - Use a **Web DAT** or **Web Browser** to publish to LiveKit using the new room
   - OR use OBS WHIP plugin to publish to the second LiveKit room

3. **Update return-viewer.html:**
   - Modify it to use `/api/processed-token` instead of `/api/viewer-token`
   - Now it will show the processed video from the second room

## Quick Start: Testing the Loop

### Fastest Path (5 minutes)

1. **In TouchDesigner:**
   - Add **NDI Out TOP** after your processing chain
   - Set **Active** to ON
   - Set **NDI Name** to "TD-Output"

2. **In OBS:**
   - Add **NDI™ Source**
   - Select "TD-Output"

3. **Start OBS Virtual Camera**
   - Tools → Virtual Camera → Start

4. **Test in browser:**
   - Open a new browser tab
   - Go to a website like `https://webcamtests.com/`
   - Select "OBS Virtual Camera" as the camera source
   - You should see your processed video!

5. **Share this with remote user:**
   - Use any video calling app (Zoom, Discord, Google Meet)
   - Select "OBS Virtual Camera" as your camera
   - Remote user sees processed video

## Troubleshooting

### "NDI Out TOP not sending"

**Solutions:**
- Make sure **Active** is checked in NDI Out TOP parameters
- Verify NDI Runtime is installed on your system
- Check that TouchDesigner is not running as administrator (NDI requires same privilege level)
- Try setting a different NDI Name and restart OBS

### "OBS doesn't show NDI source from TouchDesigner"

**Solutions:**
- Verify obs-ndi plugin is installed
- Restart OBS after starting TouchDesigner NDI Out
- Check Windows Firewall isn't blocking NDI
- Try using localhost NDI discovery instead of automatic

### "Virtual Camera shows black screen"

**Solutions:**
- Make sure the TouchDesigner source is visible in OBS preview
- Stop and restart the Virtual Camera
- Check no other application is using the Virtual Camera
- Verify your scene has the TouchDesigner source visible and not hidden

### "return-viewer.html shows original camera, not processed video"

**Expected behavior:** The current implementation connects to the same room as the input.

**Solution:** Follow Option 4 above to create a second LiveKit room for processed video, OR use Option 2 (Virtual Camera) for simpler testing.

## Next Steps

1. **For Quick Testing:** Use Option 2 (Virtual Camera) and share via video calling apps
2. **For Production:** Implement Option 4 (Second LiveKit Room) or Option 3 (RTMP Streaming)
3. **For Installation:** Set up Option 3 with a dedicated streaming service for reliability

## Additional Resources

- [NDI Documentation](https://www.ndi.tv/documentation/)
- [TouchDesigner NDI Out TOP Documentation](https://docs.derivative.ca/NDI_Out_TOP)
- [OBS NDI Plugin](https://github.com/obs-ndi/obs-ndi)
- [LiveKit WHIP Publishing](https://docs.livekit.io/guides/ingress/)

## Summary

You asked: *"its finally confirming connection to webrtc but im not sure how to 'tie' it in to my output node"*

**The answer:** 
1. Add an **NDI Out TOP** in TouchDesigner connected to your final output
2. In OBS, add an **NDI™ Source** to receive from TouchDesigner
3. Use **OBS Virtual Camera** to make it available to browsers
4. Remote users can see the processed video via video calling apps OR by implementing a second LiveKit room

The key connection is: **TouchDesigner → NDI Out TOP → OBS NDI Source → OBS Virtual Camera → Remote Viewer**
