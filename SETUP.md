# 🎥 TouchDesigner WebRTC Streaming - SIMPLE SETUP

Stream your TouchDesigner output to remote viewers with low latency.

## 🚀 Quick Start

### **1. Start the Server**
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
npm start
```

### **2. Complete the Pipeline**

#### **A. Webcam → OBS**
- Add Video Capture Device in OBS

#### **B. OBS → TouchDesigner (via NDI)**
- OBS: Tools → NDI Output Settings → ✅ Main Output
- TouchDesigner: NDI In TOP → Select OBS

#### **C. TouchDesigner Processing**
- Process your video (blue liquid effects, etc.)

#### **D. TouchDesigner → OBS (via NDI)**  
- TouchDesigner: NDI Out TOP → Send processed video back to OBS
- OBS: Add NDI Source → Select TouchDesigner output

#### **E. OBS → Web Publisher**
- OBS: Tools → Virtual Camera → Start

#### **F. Publish to Railway**
- Open: http://localhost:3000/td-publisher.html
- Click "Start OBS Virtual Camera"
- Click "Publish to Railway"

### **3. Remote Viewers Watch**
https://marvelous-blessing-production-4059.up.railway.app/

---

## 📁 Key Files

- **server.js** - WebRTC signaling server
- **td-publisher.html** - Publisher page (local)
- **viewer.html** - Remote viewer page (Railway)
- **index.html** - Main Mirror's Echo page

---

## 🔧 Troubleshooting

**"OBS Virtual Camera not found"**
- Make sure OBS Virtual Camera is started (Tools → Virtual Camera)

**"LiveKit error on Railway"**
- Hard refresh the page (Ctrl+Shift+R)
- Wait for Railway deployment to complete

**"No connection"**
- Check that server is running (`npm start`)
- Verify WebSocket connects in browser console

---

## 🎯 Deploy to Railway

```bash
git add .
git commit -m "Update WebRTC streaming"
git push
```

Railway auto-deploys from your main branch.

---

**That's it!** Low-latency WebRTC streaming from TouchDesigner to remote viewers.
