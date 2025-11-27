# MIRROR'S ECHO - HANDOVER DOCUMENT
**Date:** November 26, 2024, 8:38 PM
**Session Duration:** ~10 minutes of autonomous work

---

## ✅ WHAT WAS ACCOMPLISHED

### 1. WebRender URL Fixed
- Changed URL from Railway (`https://liquid-milk-balls-...`) to localhost
- New URL: `http://localhost:3000/td-input-viewer.html`
- Command executed in Textport:
```python
op('/webrender1').par.url = 'http://localhost:3000/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
```

### 2. Created Fixed Dual-Room HTML Page
- **File:** `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\mirrors-echo-fixed.html`
- **Key Fix:** The page now connects to TWO separate LiveKit rooms:
  - **Input Room (claymation-live):** User PUBLISHES their camera here
  - **Output Room (processed-output):** User SUBSCRIBES to see processed video from OBS

### 3. Verified TouchDesigner State
- **Project:** `MOSTWORKING.toe` is loaded
- **WebRender1:** Now showing LIVE VIDEO feed
- **Pipeline visible:** webrender1 → thresh2 → flip2 → substitute1/2 → ndiIn1

---

## 🔴 REMAINING ISSUES

### Issue 1: OBS → LiveKit Processed Output
The OBS needs to be streaming via WHIP to the `processed-output` LiveKit room.

**OBS WHIP Configuration:**
- Get fresh token: `http://localhost:3000/api/processed-publisher-token`
- Use the `whipUrl` from the response
- Format: `https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token=...`

**To verify OBS is streaming:**
1. Open: `http://localhost:3000/return-viewer.html`
2. Click "Connect"
3. If you see video, OBS is streaming correctly

### Issue 2: Website Showing Raw Camera in Both Panels
The old `mirrors-echo.html` connects to only ONE room and shows other participants.
**Solution:** Use the new `mirrors-echo-fixed.html` which:
- Publishes camera to `claymation-live` (input)
- Subscribes to `processed-output` (to see processed video)

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `MOSTWORKING.toe` | TouchDesigner project with working WebRender |
| `td-input-viewer.html` | Page WebRender loads to receive camera from LiveKit |
| `mirrors-echo-fixed.html` | **NEW** - Dual room page for end users |
| `return-viewer.html` | Simple viewer for processed-output room |
| `server/server.js` | Node.js server with all LiveKit endpoints |

---

## 🔧 QUICK COMMANDS

### Check WebRender status (paste in TD Textport):
```python
wr = op('/webrender1')
print('URL:', wr.par.url.val)
print('Size:', wr.width, 'x', wr.height)
print('MediaStream:', wr.par.mediastream.val)
```

### Get OBS WHIP Token:
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/processed-publisher-token" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Test the new page:
Open: `http://localhost:3000/mirrors-echo-fixed.html`

---

## 🎯 COMPLETE PIPELINE (Goal)

```
User's Browser Camera
    ↓ (WebRTC publish)
LiveKit Room: "claymation-live"
    ↓ (WebRTC subscribe)
TD WebRender1 (loads td-input-viewer.html)
    ↓ (TD Processing)
TD Effects Chain (thresh2 → flip2 → etc)
    ↓ (NDI Output)
OBS Studio (NDI Source)
    ↓ (WHIP Stream)
LiveKit Room: "processed-output"
    ↓ (WebRTC subscribe)
User's Browser "Processed Output" Panel
```

---

## ⚠️ NEXT STEPS FOR CONTINUATION

1. **Verify OBS WHIP streaming** - Check if OBS is publishing to processed-output room
2. **Test mirrors-echo-fixed.html** - Connect and verify both panels work
3. **If processed video not showing:**
   - Check OBS stream settings
   - Get fresh WHIP token
   - Verify OBS is using WHIP output (not RTMP)

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

**End of handover**
