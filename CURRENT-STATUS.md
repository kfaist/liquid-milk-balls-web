# 🎥 TouchDesigner Streaming - Ready to Use

## ✅ What's Running

**Local Server:** http://localhost:3000
- Process ID: 33492
- WebRTC signaling + static files

---

## 🎯 Three Pages You Have

### 1. **Publisher (You)**
http://localhost:3000/td-publisher.html

**What it does:** Publishes OBS Virtual Camera to remote viewers
**How to use:**
1. OBS → Tools → Virtual Camera → Start
2. Click "Start OBS Virtual Camera"
3. Click "Publish to Railway"

---

### 2. **Split Viewer (Original Request)**
http://localhost:3000/split-viewer.html

**What it does:** Side-by-side input/output with animated popout icon
- Left: Input camera
- Right: TouchDesigner output
- Top-right corner: Breathing icon (⤢) to fullscreen

---

### 3. **Mirror's Echo (Original Site)**
http://localhost:3000/

**What it does:** Your original beautiful site + WebRTC + popout button
- Interactive mirror
- WebRTC preview with Local/Remote video
- Popout icon appears when remote stream is active

---

## 🚀 Deploy to Railway

The site already exists at: https://marvelous-blessing-production-4059.up.railway.app/

**To update it:**
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add .
git commit -m "Add split viewer and publisher pages"
git push
```

Railway auto-deploys in ~2 minutes.

**All three pages will work on Railway:**
- https://marvelous-blessing-production-4059.up.railway.app/
- https://marvelous-blessing-production-4059.up.railway.app/split-viewer.html
- https://marvelous-blessing-production-4059.up.railway.app/td-publisher.html

---

## 📋 Complete Pipeline

```
Webcam → OBS (capture)
    ↓
OBS → NDI → TouchDesigner (process with effects)
    ↓
TouchDesigner → NDI → OBS (receive back)
    ↓
OBS → Virtual Camera
    ↓
td-publisher.html → WebRTC → Railway
    ↓
Remote viewers at Railway URL
```

---

## 🛑 Stop Server

In PowerShell where server is running: **Ctrl+C**

Or kill process:
```bash
taskkill /F /PID 33492
```

---

## 🔄 Restart Server

```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
npm start
```

---

## ✨ What's Fixed

- ✅ No more FFmpeg errors
- ✅ No more LiveKit SDK errors (using custom WebRTC)
- ✅ Clean, beautiful UI matching your site
- ✅ Split-screen viewer with animated popout
- ✅ Publisher page for TouchDesigner streaming
- ✅ Low-latency WebRTC (not RTMP)

---

**Ready to go!** 🚀
