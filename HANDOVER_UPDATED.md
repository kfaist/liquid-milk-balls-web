# MIRROR'S ECHO - UPDATED HANDOVER
**Date:** November 26, 2024, 8:55 PM

---

## ✅ COMPLETED THIS SESSION

### 1. Fixed WebRender URL (CRITICAL)
- Changed from localhost to **PRODUCTION Railway URL**
- Command executed:
```python
op('/webrender1').par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
```

### 2. Deployed `td-input-viewer.html` to Railway
- **File was missing from production deployment!**
- Created and pushed to GitHub
- Commit: `f3597eb` "Add td-input-viewer.html for TouchDesigner WebRender input"
- **Railway auto-deploy triggered - may take 1-3 minutes**

### 3. Created Dual-Room Experience Page
- File: `mirrors-echo-fixed.html` (local only, needs deployment)
- Connects to BOTH rooms:
  - Publishes camera to `claymation-live`
  - Subscribes to `processed-output` for processed video

---

## 🔴 VERIFICATION NEEDED

### Check if Railway deployed:
```powershell
Invoke-WebRequest -Uri "https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html" -Method Head
```
- If 200: Reload WebRender in TouchDesigner
- If 404: Wait more or check Railway dashboard

### Reload TouchDesigner WebRender:
```python
op('/webrender1').par.reload.pulse()
```

---

## 🎯 COMPLETE PIPELINE

```
Remote User Browser
    ↓ publishes camera to
LiveKit Room: "claymation-live"
    ↓ subscribed by
TD WebRender (loads td-input-viewer.html from Railway)
    ↓ processes video
TD Effects Chain
    ↓ outputs via
NDI to OBS
    ↓ streams via WHIP to
LiveKit Room: "processed-output"
    ↓ subscribed by
Remote User Browser (sees processed reflection)
```

---

## 📋 KEY URLS

| URL | Purpose |
|-----|---------|
| `https://liquid-milk-balls-web-production-2e8c.up.railway.app/` | Main site |
| `.../td-input-viewer.html` | TD WebRender loads this (NEW - just deployed) |
| `.../publisher.html` | Users publish camera here |
| `.../return-viewer.html` | Users view processed output |

---

## 🔧 TOUCHDESIGNER SETTINGS

- **Project:** MOSTWORKING.2.toe
- **WebRender1 URL:** `https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html`
- **Enable Media Stream:** ON
- **Active:** ON

---

## ⚠️ IF VIDEO STILL NOT SHOWING

1. Check Railway deployment status
2. Verify publishers exist in claymation-live room:
```javascript
// Run with: node check-room.js
const { RoomServiceClient } = require('livekit-server-sdk');
// Check participants in claymation-live
```

3. Check browser console in td-input-viewer.html for errors

---

**LiveKit Rooms Active:**
- `claymation-live`: 5 participants (3 with video)
- `processed-output`: OBS WHIP publisher active
