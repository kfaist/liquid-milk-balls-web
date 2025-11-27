# MIRROR'S ECHO - HANDOVER DOCUMENT
**Date:** November 26, 2024, 9:34 PM
**Project:** MOSTWORKING.2.toe

---

## ✅ CURRENT STATE

### WebRender Configuration:
- **URL:** `https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html`
- **Enable Media Stream:** On
- **Status:** Page loads, shows green status bar, black video area (waiting for video)

### LiveKit Rooms (VERIFIED ACTIVE):
**claymation-live (input room):**
- test-1764200883576 - 1 video track ✅
- test-1764200896869 - 1 video track ✅

**processed-output (output room):**
- obs-whip-publisher - OBS streaming ✅

### Files Deployed to Railway:
- ✅ `mirrors-echo-fixed.html` - Dual room page (camera + processed output)
- ✅ `td-input-viewer.html` - Auto-connecting viewer for TouchDesigner

---

## 🔴 CURRENT ISSUE

The WebRender loads `td-input-viewer.html` correctly and shows connection status, but video is not displaying even though there ARE active publishers with video tracks in the room.

**Possible causes:**
1. WebRender browser may need camera permissions granted
2. The page might be erroring on connection (check the green status bar message)
3. LiveKit track subscription issue

---

## 🎯 COMPLETE PIPELINE (Goal)

```
Remote Browser Camera
    ↓ Publish to LiveKit
claymation-live room (has 2 active video publishers!)
    ↓ Subscribe
TD WebRender (td-input-viewer.html from Railway)
    ↓ Video displayed
TD Effects Processing
    ↓ NDI Out
OBS Studio
    ↓ WHIP Stream
processed-output room (obs-whip-publisher active!)
    ↓ Subscribe
User's Browser (mirrors-echo-fixed.html)
    ↓ Shows processed video
```

---

## 📋 QUICK COMMANDS FOR NEXT SESSION

### Check/Set WebRender URL (paste in TD Textport):
```python
# Check current URL
print(op('/webrender1').par.url.val)

# Set correct URL
op('/webrender1').par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
```

### Check LiveKit room status:
```powershell
node -e "
const { RoomServiceClient } = require('./node_modules/livekit-server-sdk');
const client = new RoomServiceClient('wss://claymation-transcription-l6e51sws.livekit.cloud', 'APITw2Yp2Tv3yfg', 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW');
client.listParticipants('claymation-live').then(p => p.forEach(x => console.log(x.identity, x.tracks.length)));
"
```

---

## 📁 KEY FILES

| File | Location | Purpose |
|------|----------|---------|
| MOSTWORKING.2.toe | TD Projects/Backup/ | Current TD project |
| td-input-viewer.html | liquid-milk-balls-web/ | Auto-connecting LiveKit viewer for WebRender |
| mirrors-echo-fixed.html | liquid-milk-balls-web/ | Dual room page (deployed to Railway) |
| server/server.js | liquid-milk-balls-web/server/ | Node.js server with LiveKit endpoints |

---

## 🔑 LIVEKIT CREDENTIALS

```
URL: wss://claymation-transcription-l6e51sws.livekit.cloud
API Key: APITw2Yp2Tv3yfg
API Secret: eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
Input Room: claymation-live
Output Room: processed-output
```

---

## 🚀 NEXT STEPS

1. **Debug why WebRender isn't showing video** despite active publishers
   - Check browser console in WebRender (if possible)
   - Verify td-input-viewer.html works in regular browser first
   - May need to reload or restart WebRender

2. **Test end-to-end with mirrors-echo-fixed.html**
   - Open: https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo-fixed.html
   - Left panel: Your camera
   - Right panel: Processed video from OBS

3. **If video still doesn't show in WebRender:**
   - Try different WebRender resolution settings
   - Check if CORS or permissions are blocking
   - Test with a simpler page first
