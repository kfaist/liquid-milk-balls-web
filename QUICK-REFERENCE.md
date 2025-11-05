# 🎯 QUICK REFERENCE - Remote Camera System

## 📱 REMOTE USER (Send Camera)
**URL:** https://marvelous-blessing-production-4059.up.railway.app/

**Steps:**
1. Click "Start Camera" → Allow
2. Click "Start WebRTC Call" → Wait for green checkmark
3. Status: "🎥 Live! Your camera is streaming..."

---

## 🎬 YOU IN OBS (Receive Camera)

**Browser Source Settings:**
- **URL:** `https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html`
- **Width:** 1920 | **Height:** 1080
- ✅ Shutdown source when not visible
- ✅ Refresh browser when scene becomes active

---

## 🔧 NDI TO TOUCHDESIGNER

**OBS:**
- Tools → NDI Output Settings → ✅ Main Output

**TouchDesigner:**
- NDI In TOP → Select "KRISTA-SHOWPUTER-01 (OBS)"

---

## 📺 OUTPUT TO SCREEN 2

**OBS:**
- Right-click scene → Fullscreen Projector (Scene) → Screen 2

---

## ⚠️ TROUBLESHOOTING

**No video in OBS?**
→ Remote user needs to click "Start WebRTC Call"
→ Right-click Browser Source → Refresh

**No NDI in TouchDesigner?**
→ Check OBS NDI Output is enabled
→ Restart TouchDesigner

**Camera won't start?**
→ Check browser permissions (should be HTTPS)
→ Try different browser (Chrome recommended)

---

## 🔗 QUICK LINKS

**Railway Dashboard:** https://railway.com/project/bd63cb55-e6cf-4def-9b37-fd29d7f36605
**LiveKit Dashboard:** https://cloud.livekit.io/projects/p_3ou36xol2x7/sessions
**Publisher Page:** https://marvelous-blessing-production-4059.up.railway.app/
**Viewer Page:** https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html

---

## ✅ PRE-SHOW CHECKLIST

- [ ] Railway deployment: GREEN
- [ ] OBS Browser Source: ADDED
- [ ] NDI Output: ENABLED
- [ ] TouchDesigner NDI In: CONNECTED
- [ ] Screen 2 Projector: SET
- [ ] Remote user has URL
- [ ] Test connection: SUCCESS

**Room Name:** claymation-live (or your custom name in Railway vars)
