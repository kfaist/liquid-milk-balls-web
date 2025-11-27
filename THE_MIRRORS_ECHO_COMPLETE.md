# 🎉 THE MIRROR'S ECHO - COMPLETE & WORKING!
**Date:** November 26, 2024
**Status:** ✅ FULLY OPERATIONAL

---

## 🌐 USER URL

**`https://adequate-balance-production.up.railway.app/`**

Users visit, click Connect, and experience their transformed reflection!

---

## ✅ COMPLETE PIPELINE

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER'S PHONE/BROWSER                                               │
│  ┌─────────────┐                          ┌─────────────────────┐   │
│  │ Camera+Audio│ ──────────────────────── │ Processed Video     │   │
│  │ (Left Panel)│                          │ (Right Panel)       │   │
│  └─────────────┘                          └─────────────────────┘   │
└────────┬────────────────────────────────────────────▲───────────────┘
         │ WebRTC Publish                             │ WebRTC Subscribe
         ▼                                            │
┌─────────────────────┐                    ┌─────────────────────┐
│ LiveKit Cloud       │                    │ LiveKit Cloud       │
│ "claymation-live"   │                    │ "processed-output"  │
│ (Input Room)        │                    │ (Output Room)       │
└─────────┬───────────┘                    └──────────▲──────────┘
          │ WebRTC Subscribe                          │ WHIP Publish
          ▼                                           │
┌─────────────────────────────────────────────────────┴───────────────┐
│  YOUR SHOWPUTER                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ TouchDesigner│───▶│   Effects    │───▶│   NDI Out    │          │
│  │  WebRender   │    │ (Your Magic) │    │              │          │
│  └──────────────┘    └──────────────┘    └──────┬───────┘          │
│                                                  │ NDI              │
│                                          ┌───────▼───────┐          │
│                                          │  OBS Studio   │──────────┘
│                                          │  (WHIP Out)   │
│                                          └───────────────┘
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 TECHNICAL CONFIGURATION

### TouchDesigner WebRender
- **URL:** `https://adequate-balance-production.up.railway.app/td-input-viewer.html`
- **Enable Media Stream:** On
- **Project:** `C:\Users\krista-showputer\Desktop\TD Projects\Backup\MOSTWORKING.2.toe`

### OBS WHIP Streaming
- **Service:** WHIP
- **Get fresh token:** `https://adequate-balance-production.up.railway.app/api/processed-publisher-token`
- **Use the `whipUrl` value from that response**

### LiveKit Rooms
| Room | Purpose |
|------|---------|
| `claymation-live` | Users publish camera here, TD subscribes |
| `processed-output` | OBS publishes here, users subscribe |

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `server.js` | Node server with all API endpoints |
| `mirrors-echo-fixed.html` | Main dual-room experience (served at `/`) |
| `td-input-viewer.html` | Auto-connecting viewer for WebRender |
| `MOSTWORKING.2.toe` | TouchDesigner project with effects |

---

## 🔑 API ENDPOINTS

Base: `https://adequate-balance-production.up.railway.app`

| Endpoint | Purpose |
|----------|---------|
| `/api/viewer-token` | Subscribe to input room |
| `/api/publisher-token` | Publish to input room |
| `/api/processed-viewer-token` | Subscribe to output room |
| `/api/processed-publisher-token` | Publish to output room + WHIP URL |

---

## 🛠️ TROUBLESHOOTING

### WebRender not showing video:
```python
# In TD Textport:
op('/webrender1').par.reload.pulse()
```

### Check LiveKit rooms:
```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
node -e "require('./node_modules/livekit-server-sdk').RoomServiceClient('wss://claymation-transcription-l6e51sws.livekit.cloud','APITw2Yp2Tv3yfg','eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW').listRooms().then(r=>console.log(r.map(x=>x.name)))"
```

### OBS not connecting:
1. Get fresh WHIP token from `/api/processed-publisher-token`
2. Copy the full `whipUrl` value
3. Paste into OBS Stream settings

---

## 🔐 LIVEKIT CREDENTIALS

```
URL: wss://claymation-transcription-l6e51sws.livekit.cloud
API Key: APITw2Yp2Tv3yfg
API Secret: eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
```

---

## 🎨 THE EXPERIENCE

1. User visits `https://adequate-balance-production.up.railway.app/`
2. Clicks **Connect**
3. Grants camera permission
4. **Left panel:** Their live camera feed
5. **Right panel:** Their reflection, transformed through your TouchDesigner effects
6. Magic happens! ✨

---

## 📝 SESSION FIXES SUMMARY

1. **Fixed WebRender URL** - Changed from localhost to production Railway URL
2. **Added /api/ endpoints** - Server was missing the token endpoints the HTML pages needed
3. **Fixed existing participant detection** - Browser now finds OBS track even if it connected first
4. **Updated root URL** - Main page now serves the dual-room experience

---

**Created with love for The Mirror's Echo** 🪞✨
