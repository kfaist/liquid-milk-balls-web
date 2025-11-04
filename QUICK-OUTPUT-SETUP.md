# Quick Answer: Connecting WebRTC to Your TouchDesigner Output Node

## You Asked: "its finally confirming connection to webrtc but im not sure how to 'tie' it in to my output node"

### The Answer (2 minutes):

You need to **send the processed video FROM TouchDesigner back TO OBS**, then make it available to viewers.

```
WebRTC Camera → OBS → NDI → TouchDesigner → [YOUR OUTPUT NODE] → NDI → OBS → Viewer
                                            ↑ YOU ARE HERE
```

## Quick Setup (3 Steps):

### Step 1: In TouchDesigner
1. Add **NDI Out TOP** operator after your final output
2. Connect your processed video to it
3. Set these parameters:
   - **Active**: ✅ ON
   - **NDI Name**: "TD-Output" (or any name you want)

### Step 2: In OBS
1. Add new source: **NDI™ Source**
2. Select **"COMPUTER-NAME (TD-Output)"** from dropdown
3. Done! Your processed video is now in OBS

### Step 3: Get It Back to Remote User's Web Browser

**For video calling apps (Zoom, Discord):**
- OBS → Tools → Start Virtual Camera
- Share using "OBS Virtual Camera" as your camera

**For web browser viewing (return-viewer.html):**
- You need OBS to publish to a second LiveKit room
- Remote user opens return-viewer.html and sees processed video
- **See [WEB-BROWSER-RETURN-PATH.md](WEB-BROWSER-RETURN-PATH.md) for complete setup**

**For streaming services:**
- Stream to YouTube Live (unlisted) or Mux
- Give remote user the viewing URL

## That's It!

Your connection is now complete:
1. ✅ Remote camera comes IN via WebRTC
2. ✅ You process it in TouchDesigner
3. ✅ It goes back OUT via NDI to OBS
4. ✅ Remote user sees the result

## Troubleshooting

**"NDI Out TOP not working"**
- Make sure **Active** is checked
- Restart OBS after enabling NDI Out in TouchDesigner

**"OBS doesn't see TD NDI source"**
- Check NDI Runtime is installed
- Both apps must have same admin privileges
- Try a different NDI Name

**"How does it get back in the web browser?"**
- You need OBS to publish to a second LiveKit room
- Install OBS WHIP plugin and configure it to stream to LiveKit
- return-viewer.html connects to the second room with processed video
- **See [WEB-BROWSER-RETURN-PATH.md](WEB-BROWSER-RETURN-PATH.md) for step-by-step instructions**

## Full Documentation

For more options and detailed setup:
- 📖 [TOUCHDESIGNER-OUTPUT-GUIDE.md](TOUCHDESIGNER-OUTPUT-GUIDE.md) - Complete guide with all options
- 📖 [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and flow diagrams
- 📖 [WEBRTC-SETUP.md](WEBRTC-SETUP.md) - WebRTC and NDI setup
