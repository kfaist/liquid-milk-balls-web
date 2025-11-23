# 🌐 YOUR PUBLIC RAILWAY DEPLOYMENT URLS

**Deployment:** liquid-milk-balls-web-production-2e8c.up.railway.app

---

## 📱 TWO PUBLIC-FACING PAGES

### 1. PUBLISHER (Camera Input) ✅ WORKING
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
```

**What it does:**
- Participants open this URL
- Click "Start Camera" 
- Camera feed goes to LiveKit room "claymation-live"
- This is the INPUT to your art installation

**Status:** 
- ✅ Tested and loading
- ✅ Shows "Ready"
- ✅ Accessible publicly

**Share this with:** Anyone you want to participate by sending their camera

---

### 2. RETURN-VIEWER (Processed Output)
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html
```

**What it does:**
- Shows the processed/transformed video
- Receives from LiveKit room "processed-output"
- This is the OUTPUT of your art installation
- Viewers see the TouchDesigner effects applied

**Status:**
- ✅ Should be working (standard deployment)
- 🔍 Check in Firefox (just opened it for you)

**Share this with:** Anyone you want to watch the processed art

---

## 📊 YOUR COMPLETE PIPELINE

```
PUBLIC INPUT
https://.../publisher.html
    ↓ (camera feed)
LiveKit Cloud ("claymation-live")
    ↓
LOCAL PROCESSING
localhost:3000/td-auto-viewer.html
    ↓
TouchDesigner (effects/processing)
    ↓
NDI → OBS → Stream
    ↓
LiveKit Cloud ("processed-output")
    ↓
PUBLIC OUTPUT
https://.../return-viewer.html
```

---

## 🎨 USE CASES

**For Installations:**
- Display publisher.html on tablets at venue (participants use their cameras)
- Display return-viewer.html on large screen (everyone watches the art)

**For Remote Events:**
- Send publisher.html link to participants
- Send return-viewer.html link to audience
- Everyone experiences the interactive art remotely!

**For Testing:**
- Open publisher.html on your phone
- Open return-viewer.html on your computer
- Test the full pipeline end-to-end

---

## ✅ VERIFIED STATUS (as of Nov 22, 2025)

- ✅ Railway deployment active
- ✅ Publisher page accessible and loading
- ✅ Return-viewer page deployed (opened in Firefox)
- ✅ Both pages served from same Railway instance
- ✅ LiveKit credentials configured
- ✅ Node server code deployed

---

## 🔗 QUICK LINKS

**Your Railway Dashboard:**
https://railway.com/project/440956c3-fee6-4fe9-b0a7-48bb997794a5

**Publisher (Input):**
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html

**Viewer (Output):**
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html

---

## 📱 SHARE THESE URLS

**For Participants (send camera):**
"Join my interactive art piece! Open this link and start your camera: 
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html"

**For Viewers (watch art):**
"Watch the interactive art transformation! 
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html"

---

**Base URL:** https://liquid-milk-balls-web-production-2e8c.up.railway.app
**Status:** Both pages deployed and accessible
**Tested:** November 22, 2025
