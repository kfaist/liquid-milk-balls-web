# 🎥 HANDOFF: Remote Webcam → TouchDesigner Pipeline

## 📍 CURRENT STATUS

**Waiting for Railway deployment** (~2 minutes remaining)

**Project:** Remote camera streaming to TouchDesigner for visual processing  
**Goal:** Get remote user's webcam → OBS → NDI → TouchDesigner → Screen 2  
**Status:** Video pipeline configured, waiting for fresh deployment without LiveKit cache

---

## 🎯 THE PIPELINE (What We're Building)

```
Remote User's Phone/Laptop (Webcam)
    ↓ WebRTC
OBS Browser Source (viewer.html)
    ↓ NDI Output
TouchDesigner NDI In TOP
    ↓ [User's Visual Processing Here]
TouchDesigner Window COMP
    ↓
Screen 2 (Full Screen Output)
```

---

## ✅ WHAT'S READY

### **1. Remote Camera Publisher (Phone/Laptop)**
**URL:** https://marvelous-blessing-production-4059.up.railway.app/  
**Status:** ✅ Ready (custom WebRTC with signaling server)

**User does:**
1. Opens URL on phone
2. Clicks "Start Camera" → Grants permission
3. Clicks "Start WebRTC Call" → Publishes to signaling server

---

### **2. OBS Browser Source (Receiver)**
**URL:** https://marvelous-blessing-production-4059.up.railway.app/viewer.html  
**Status:** ✅ Just created (clean, no LiveKit cache issues)

**Features:**
- Full-screen video only (no UI clutter)
- Auto-connects to signaling server
- Shows remote camera when user connects
- Black background for clean keying

**OBS Setup:**
- Add Browser Source
- URL: viewer.html (see above)
- Width: 1920, Height: 1080
- ✅ "Shutdown source when not visible"

---

### **3. OBS NDI Output**
**Status:** ✅ Ready to enable

**Steps:**
1. OBS → Tools → NDI Output Settings
2. ✅ Check "Main Output"
3. (Optional) Name: "OBS-Remote-Camera"

This broadcasts OBS output over local network via NDI protocol.

---

## 🎨 TOUCHDESIGNER SETUP (Input → Process → Output)

### **INPUT: Get Video from OBS**

**Add NDI In TOP:**
1. Create **NDI In TOP** operator
2. Parameters → **NDI Source** dropdown
3. Select: **"KRISTA-SHOWPUTER-01 (OBS)"**
4. Should show remote camera video

**Troubleshooting NDI:**
- ✅ NDI Runtime installed on Windows
- ✅ OBS NDI Output enabled
- ✅ Same local network
- ✅ Windows Firewall allows NDI (ports 5353, 5960)

---

### **PROCESSING: [User's Creative Work]**

Connect NDI In TOP → User's processing network (effects, AI, generative visuals, etc.)

**Not covered in this handoff - user handles their creative pipeline.**

---

### **OUTPUT: Send to Screen 2**

**Method 1: Window COMP (Recommended)**
1. Add **Window COMP** operator
2. Connect processed video → Window COMP input
3. Parameters:
   - **Borders:** Off
   - **Monitor:** Select Screen 2
   - **Full Screen:** On
   - **Open in Perform Mode:** On

**Method 2: Perform Mode Projector**
1. Right-click in TouchDesigner
2. **Perform Mode**
3. Drag window to Screen 2
4. Alt+Enter for fullscreen

---

## 🚨 CURRENT ISSUE & FIX

**Problem:** Browser cache showing old LiveKit error  
**Solution:** Fresh viewer.html page (no cache history) + Railway redeployment

**Files cleaned:**
- ✅ Deleted livekit-publisher.js
- ✅ index.html only loads webrtc-client.js
- ✅ viewer.html is brand new (no LiveKit)

**Deployment in progress:** commit `bade211` - removes all LiveKit remnants

---

## 🧪 TESTING SEQUENCE (After Railway Deploys)

### **Step 1: Test Publisher (Phone)**
```
https://marvelous-blessing-production-4059.up.railway.app/
```

**Expected:**
- Click "Start Camera" → Camera preview appears
- Click "Start WebRTC Call" → "Connected to signaling server"
- Status: NOT "LiveKit SDK not loaded"

**If still shows LiveKit error:**
- Force close browser completely
- Try cache buster: `?cachebust=20251104`

---

### **Step 2: Test Viewer (OBS)**
```
https://marvelous-blessing-production-4059.up.railway.app/viewer.html
```

**Expected:**
- Page loads with black background
- Status: "🔄 Connecting to signaling server..."
- Then: "✅ Connected - Waiting for remote camera..."
- When publisher connects: Shows their camera full-screen

**OBS Browser Source Settings:**
- URL: viewer.html (above)
- Width: 1920, Height: 1080

---

### **Step 3: Enable NDI in OBS**

**OBS → Tools → NDI Output Settings → ✅ Main Output**

Verify in TouchDesigner:
- NDI In TOP → Source dropdown should show "KRISTA-SHOWPUTER-01 (OBS)"

---

### **Step 4: Connect TouchDesigner**

**Quick Test:**
1. NDI In TOP → Select OBS source
2. Should see remote camera
3. Connect to processing network
4. Output to Screen 2 via Window COMP

---

## 🔧 TECHNICAL DETAILS

**Architecture:** Custom WebRTC (free, peer-to-peer with signaling)  
**Signaling Server:** WebSocket at `wss://marvelous-blessing.../ws`  
**STUN Server:** `stun:stun.l.google.com:19302`  
**NDI:** Local network protocol (no internet required after WebRTC receives)

**File Locations:**
- Project: `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web`
- GitHub: https://github.com/kfaist/liquid-milk-balls-web
- Railway: https://railway.com/project/bd63cb55-e6cf-4def-9b37-fd29d7f36605

**Key Files:**
- `viewer.html` - Clean full-screen viewer for OBS (NEW)
- `index.html` - Publisher UI for remote user
- `webrtc-client.js` - WebRTC peer connection logic
- `server.js` - WebSocket signaling server

---

## ⚠️ KNOWN LIMITATIONS

**Network Requirements:**
- WebRTC works peer-to-peer (direct connection between devices)
- May not work behind some firewalls/NATs without TURN server
- If connection fails, both devices should be on same network for testing

**NDI Requirements:**
- Works on local network only
- Uses ~100-250 Mbps bandwidth
- May be blocked by Windows Firewall (check settings)

---

## 🎯 SUCCESS CRITERIA

✅ Remote user's camera streams to their browser  
✅ OBS Browser Source displays remote camera  
✅ OBS NDI Output enabled  
✅ TouchDesigner NDI In TOP receives video  
✅ TouchDesigner processes video (user's creative work)  
✅ Processed video displays full-screen on Screen 2  

---

## 💡 NEXT CONVERSATION SHOULD FOCUS ON:

1. **Verify viewer.html works** (should be clean, no LiveKit cache)
2. **Test WebRTC connection** (phone → OBS)
3. **Confirm NDI reception** in TouchDesigner
4. **Set up Window COMP** for Screen 2 output

**DO NOT focus on:** TouchDesigner processing details (user handles that)

---

## 📱 USER CONTEXT

**User:** Krista - VR/AI artist, dyslexic, needs step-by-step instructions  
**Project:** "The Mirror's Echo" - Interactive AI projection installation  
**Experience Level:** Comfortable with TouchDesigner, needs guidance on networking/WebRTC  
**Preference:** Direct, actionable steps over theoretical explanations

---

## 🚀 IMMEDIATE ACTION ITEMS

**Right now (waiting for Railway):**
- Nothing to do, let deployment finish (~2 minutes)

**Once deployed:**
1. Test viewer.html in browser (should work cleanly)
2. Add to OBS as Browser Source
3. Test phone → OBS connection
4. Enable NDI in OBS
5. Connect NDI In TOP in TouchDesigner
6. Verify video appears
7. Connect to processing network
8. Output to Screen 2

---

## 🆘 IF STUCK

**WebRTC not connecting:**
- Check browser console for errors
- Verify WebSocket connection in Network tab
- Try both devices on same WiFi network

**NDI not appearing in TouchDesigner:**
- Verify OBS NDI Output is enabled
- Check Windows Firewall isn't blocking NDI
- Restart TouchDesigner
- Check NDI monitor/test tools

**Video quality issues:**
- Adjust WebRTC constraints in webrtc-client.js
- Check network bandwidth
- Lower OBS output resolution

---

## ✨ THE GOAL

**Get remote camera into TouchDesigner so user can do their creative magic, then output to Screen 2 for their installation.**

Everything before TouchDesigner processing (WebRTC → OBS → NDI) and after processing (Window COMP → Screen 2) should be automated and reliable.

User focuses on the art, not the plumbing.
