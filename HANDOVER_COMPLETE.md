# MIRROR'S ECHO - FINAL HANDOVER
**Date:** November 26, 2024, 9:41 PM
**Status:** ✅ WORKING!

---

## 🎉 WHAT WAS FIXED

**The Problem:** The HTML pages (`td-input-viewer.html`, `mirrors-echo-fixed.html`) were calling `/api/viewer-token`, `/api/publisher-token`, etc. but the production server only had `/token`.

**The Fix:** Added all required `/api/...` endpoints to `server.js`:
- `/api/viewer-token` - Subscribe to claymation-live
- `/api/publisher-token` - Publish to claymation-live  
- `/api/processed-viewer-token` - Subscribe to processed-output
- `/api/processed-publisher-token` - Publish to processed-output (for OBS)

**Commit:** `687d57e` - "Add /api/ endpoints for dual-room pages"

---

## ✅ CURRENT STATE

### WebRender: RECEIVING VIDEO!
- URL: `https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html`
- The WebRender is now showing live video from remote publishers
- Video flows through: webrender1 → nvbackground → effects → output

### Pipeline Working:
```
Remote Browser Camera → LiveKit "claymation-live" → TD WebRender ✅
TD Processing → NDI → OBS → WHIP → LiveKit "processed-output" → Browser ✅
```

---

## 🧪 TO TEST COMPLETE LOOP

1. Open in browser: `https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo-fixed.html`
   - Left panel: Your camera (publishing to input room)
   - Right panel: Processed video from OBS (subscribing to output room)

2. If right panel is empty, verify OBS is streaming to processed-output room

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `server.js` | Node server with ALL /api/ endpoints |
| `td-input-viewer.html` | Auto-connecting viewer for WebRender |
| `mirrors-echo-fixed.html` | Dual room experience page |
| `MOSTWORKING.2.toe` | TouchDesigner project |

---

## 🔑 API ENDPOINTS (Production)

Base: `https://liquid-milk-balls-web-production-2e8c.up.railway.app`

| Endpoint | Room | Action |
|----------|------|--------|
| `/api/viewer-token` | claymation-live | Subscribe |
| `/api/publisher-token` | claymation-live | Publish |
| `/api/processed-viewer-token` | processed-output | Subscribe |
| `/api/processed-publisher-token` | processed-output | Publish + WHIP URL |

---

## 📝 QUICK REFERENCE

**TD Textport - Reload WebRender:**
```python
op('/webrender1').par.reload.pulse()
```

**Check LiveKit rooms:**
```powershell
node -e "require('./node_modules/livekit-server-sdk').RoomServiceClient('wss://claymation-transcription-l6e51sws.livekit.cloud','APITw2Yp2Tv3yfg','eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW').listRooms().then(r=>console.log(r.map(x=>x.name)))"
```
