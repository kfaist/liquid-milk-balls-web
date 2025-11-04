# 🚀 LiveKit Remote Camera System - Quick Start Guide

**Status:** ✅ Built and Deployed  
**Deployed URL:** https://marvelous-blessing-production-4059.up.railway.app/

---

## 🎯 **System Overview**

**Flow:**
```
Remote User's Camera → LiveKit Room → OBS (via ndi-viewer.html) → NDI → TouchDesigner
```

**What Changed:**
- ✅ Swapped custom P2P WebRTC → LiveKit WebRTC
- ✅ Same UI, same buttons, same user experience
- ✅ Backend now uses managed LiveKit infrastructure
- ✅ Works in OBS Browser Source (no camera permission issues!)

---

## 📋 **Prerequisites Checklist**

Before testing, make sure Railway has:
- ✅ LIVEKIT_API_KEY (added via "Add All" button)
- ✅ LIVEKIT_API_SECRET  
- ✅ LIVEKIT_ROOM_NAME
- ✅ LIVEKIT_URL
- ✅ Successful deployment (check Railway dashboard)

**Action Needed:** If you haven't clicked "Add All" in Railway Variables yet, do that now!

---

## 🎬 **TESTING WORKFLOW**

### **Step 1: Remote User Publishes Camera** (2 minutes)

**Remote user opens:**
```
https://marvelous-blessing-production-4059.up.railway.app/
```

**They do:**
1. Click **"Start Camera"** → Grant camera permission
2. Click **"Start WebRTC Call"** → Publishes to LiveKit room
3. Status shows: "🎥 Live! Your camera is streaming to OBS via LiveKit"

**Note:** The button still says "Start WebRTC Call" - that's correct! LiveKit IS WebRTC.

---

### **Step 2: You Receive in OBS** (3 minutes)

**In OBS Studio:**

1. **Add Browser Source:**
   - Right-click in Sources → Add → Browser Source
   - Name it: "LiveKit Remote Camera"
   
2. **Configure Source:**
   - URL: `https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html`
   - Width: 1920
   - Height: 1080
   - FPS: 30
   - ✅ Check: "Shutdown source when not visible"
   - ✅ Check: "Refresh browser when scene becomes active"
   
3. **Click OK**

**You should see:**
- "Waiting for remote user..." (if nobody connected yet)
- Remote user's camera (once they click "Start WebRTC Call")

---

### **Step 3: Send to TouchDesigner via NDI** (2 minutes)

**In OBS:**
1. **Tools → NDI Output Settings**
2. Check: **"Main Output"**
3. Set name: "OBS-LiveKit-Stream" (or whatever you prefer)

**In TouchDesigner:**
1. Add **NDI In TOP** operator
2. In parameters, find **"NDI Source"** dropdown
3. Select: **"KRISTA-SHOWPUTER-01 (OBS-LiveKit-Stream)"**
4. Video should appear!

**Your NDI source shows as:** `KRISTA-SHOWPUTER-01 (TouchDesigner)` based on your screenshot

---

### **Step 4: Output to Screen 2** (1 minute)

**Option A: Fullscreen Projector**
- Right-click scene in OBS
- **Fullscreen Projector (Scene)** → Select Screen 2

**Option B: Virtual Camera**
- Tools → **Start Virtual Camera**
- Other software can capture "OBS Virtual Camera"

---

## 🔍 **TROUBLESHOOTING**

### **Remote User Issues:**

**"Failed to get LiveKit token"**
- ✅ Check Railway Variables are added
- ✅ Verify deployment succeeded
- ✅ Check browser console for errors

**"Camera permission denied"**
- User needs to click "Allow" when browser asks
- Try different browser (Chrome recommended)
- Check site isn't blocked by browser settings

**"Connection failed"**
- Check LiveKit account isn't over limits (you hit 108/100 recently)
- Verify LIVEKIT_URL is correct format: `wss://...livekit.cloud`
- Check Railway logs for errors

---

### **OBS Issues:**

**Browser Source shows error:**
- Verify URL is exactly: `/ndi-viewer.html`
- Check "Shutdown source when not visible" is checked
- Try right-click → Refresh

**"Waiting for video..." stuck:**
- Remote user needs to click "Start WebRTC Call"
- Check they're in the same LiveKit room
- Verify room name matches in both places

**No video appearing:**
- Check browser source is added and visible
- Verify remote user successfully connected
- Look for errors in OBS log files

---

### **NDI Issues:**

**TouchDesigner doesn't see NDI source:**
- ✅ Verify NDI Runtime is installed
- ✅ Check OBS NDI Output is enabled
- ✅ Restart TouchDesigner if needed
- ✅ Check Windows Firewall isn't blocking NDI

**Video is laggy/choppy:**
- Lower OBS output resolution
- Check network bandwidth (NDI uses ~100-250 Mbps)
- Use wired connection instead of WiFi if possible

---

## 📊 **MONITORING**

### **Railway Logs:**
```bash
# Check if LiveKit is connecting
Look for: "[publisher-token] Generated for publisher-xxxx"
```

### **LiveKit Dashboard:**
https://cloud.livekit.io/projects/p_3ou36xol2x7/sessions
- Should show active sessions
- Monitor participant count
- Check connection quality

### **OBS Stats:**
- Right-click OBS preview → Stats
- Check "Frames Missed" (should be 0)
- Monitor CPU usage

---

## 🎨 **CUSTOMIZATION OPTIONS**

### **Change Room Name:**
Set in Railway Variables:
```
LIVEKIT_ROOM_NAME=my-custom-room-name
```

### **Change Video Quality:**
Edit `livekit-publisher.js`:
```javascript
videoCaptureDefaults: {
    resolution: LivekitClient.VideoPresets.h720.resolution,  // or h1080, h1440, h2160
}
```

### **Change Button Text:**
Edit `index.html` - buttons are in the WebRTC section

---

## 🔗 **USEFUL LINKS**

**Your Deployments:**
- Publisher: https://marvelous-blessing-production-4059.up.railway.app/
- Viewer: https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html
- Railway: https://railway.com/project/bd63cb55-e6cf-4def-9b37-fd29d7f36605
- LiveKit: https://cloud.livekit.io/projects/p_3ou36xol2x7/overview

**Documentation:**
- LiveKit Client SDK: https://docs.livekit.io/client-sdk-js/
- NDI Tools: https://ndi.video/tools/
- OBS NDI Plugin: https://github.com/obs-ndi/obs-ndi

---

## 📱 **TESTING CHECKLIST**

Before your next performance/installation:

- [ ] Railway variables are added
- [ ] Deployment succeeded (green checkmark)
- [ ] Remote user can access URL on their device
- [ ] Remote user can grant camera permission
- [ ] "Start WebRTC Call" connects successfully
- [ ] OBS Browser Source shows video
- [ ] NDI output is enabled in OBS
- [ ] TouchDesigner receives NDI feed
- [ ] Screen 2 displays output
- [ ] Audio is working (if needed)

---

## 🆘 **EMERGENCY FALLBACK**

If LiveKit fails during performance:

**Option 1: Window Capture**
1. Open publisher URL in regular Chrome
2. Full screen the video
3. OBS: Window Capture → Chrome window

**Option 2: Custom WebRTC**
1. In Railway Variables, remove LiveKit vars
2. Falls back to peer-to-peer WebRTC
3. Limited to local network

---

## 🎉 **YOU'RE READY!**

Everything is deployed and ready to test. 

**Next step:** Click "Add All" in Railway Variables (if not done), wait 2 minutes for deployment, then test the flow!

**Questions?** Check Railway logs or LiveKit dashboard for diagnostics.
