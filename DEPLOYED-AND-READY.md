# 🎨 The Mirror's Echo - DEPLOYED & READY

**Deployment Status:** ✅ LIVE on Railway  
**Deployed:** November 4, 2025  
**What Changed:** Two-room bidirectional streaming architecture

---

## 🌐 Live URLs

### For Remote Participants:
**https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html**

What they see:
- LEFT (BIG): Your processed TouchDesigner output with breathing popout button ⤢
- RIGHT (small): Their own webcam preview
- Click "Start Camera" to begin

### For You (Krista):
**https://marvelous-blessing-production-4059.up.railway.app/krista-studio.html**

What you see:
- FULLSCREEN clean video - pixel-to-pixel
- No UI, no buttons, just their camera filling your screen
- Auto-connects to receive their input

### Your Publisher:
**https://marvelous-blessing-production-4059.up.railway.app/td-publisher.html**

What it does:
- Broadcasts your OBS Virtual Camera to output-room
- Remote participants receive this stream

---

## 🎯 Complete Workflow (Step-by-Step)

### Your Setup (Before Session):

1. **Open your studio view:**
   - Go to: https://marvelous-blessing-production-4059.up.railway.app/krista-studio.html
   - This fullscreen video shows their input when they connect

2. **Start OBS:**
   - Tools → Virtual Camera → Start

3. **Open publisher:**
   - Go to: https://marvelous-blessing-production-4059.up.railway.app/td-publisher.html
   - Click "Start OBS Virtual Camera"
   - Click "Publish to Railway"

4. **Send participant the link:**
   - https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html

---

### Participant Flow:

1. Opens your link (remote-participant.html)
2. Clicks "Start Camera" 
3. Allows webcam access
4. **Their camera instantly streams to YOU**
5. **They see YOUR processed output (big, beautiful display)**

---

### Your Processing Loop:

```
Participant's camera 
    ↓
YOUR SCREEN: krista-studio.html (fullscreen view)
    ↓
OBS captures this input
    ↓
NDI → TouchDesigner (your effects/processing)
    ↓
NDI back to OBS
    ↓
Virtual Camera → td-publisher.html
    ↓
Broadcast to output-room
    ↓
Participant sees result on their LEFT panel
```

---

## 🎨 Features

**Remote Participant Page:**
- ✅ Beautiful design matching your Mirror's Echo aesthetic
- ✅ Big display (2/3 screen) for your processed art
- ✅ Breathing popout button (⤢) top-left corner
- ✅ Fullscreen overlay with "Pop Out to Window" option
- ✅ Small webcam preview (1/3 screen) top-right
- ✅ Auto-reconnect if connection drops

**Your Studio Page:**
- ✅ Clean fullscreen video (pixel-to-pixel)
- ✅ No UI elements - just video
- ✅ Black background
- ✅ Auto-connects when participant joins
- ✅ Perfect for capture in OBS

**Technical:**
- ✅ Room-based WebRTC (input-room + output-room)
- ✅ Low-latency streaming
- ✅ Auto-reconnect on both sides
- ✅ No external dependencies

---

## 📱 How to Use

### Quick Start (For a Session):

1. **Open 3 tabs:**
   - Tab 1: https://marvelous-blessing-production-4059.up.railway.app/krista-studio.html
   - Tab 2: https://marvelous-blessing-production-4059.up.railway.app/td-publisher.html  
   - Tab 3: OBS (with Virtual Camera running)

2. **Start publishing:**
   - In td-publisher tab: Click "Start OBS Virtual Camera" then "Publish to Railway"

3. **Share with participant:**
   - Send them: https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html
   - Tell them to click "Start Camera"

4. **You're live!**
   - You see their input in krista-studio.html (fullscreen)
   - Process in TouchDesigner
   - They see your output (big beautiful display with popout)

---

## 🎬 OBS + TouchDesigner Pipeline

**Your Processing Chain:**
1. OBS captures krista-studio.html window (their camera)
2. OBS → NDI out → TouchDesigner
3. TouchDesigner applies your effects
4. TouchDesigner → NDI out → OBS
5. OBS → Virtual Camera
6. td-publisher.html broadcasts Virtual Camera
7. Participant receives processed stream

---

## 🔧 Troubleshooting

**Participant sees black screen:**
- Make sure you're publishing from td-publisher.html
- Check OBS Virtual Camera is running
- Refresh their page

**You see black screen:**
- Participant needs to click "Start Camera"
- Check their browser allowed webcam access
- Refresh your krista-studio.html

**Connection drops:**
- Pages auto-reconnect every 3 seconds
- Just wait, connection will restore

**Video quality issues:**
- Check OBS bitrate settings
- Verify network connection on both sides

---

## 📂 File Structure

```
liquid-milk-balls-web/
├── index.html                  # Original Mirror's Echo site
├── remote-participant.html     # NEW: Viewer page (for participants)
├── krista-studio.html         # NEW: Your fullscreen studio view
├── td-publisher.html          # OBS broadcaster (unchanged)
├── server.js                  # NEW: Room-based signaling
├── TWO-ROOM-SETUP.md         # Technical documentation
└── DEPLOYED-AND-READY.md     # This file
```

---

## 🎯 What's Next?

1. **Test it out:**
   - Open remote-participant.html in one browser
   - Open krista-studio.html in another
   - Click "Start Camera" and verify connection

2. **Try the full pipeline:**
   - Add OBS + TouchDesigner to the mix
   - Test the complete loop

3. **Share with a real participant:**
   - Send them the remote-participant.html link
   - Walk them through clicking "Start Camera"

---

## ✨ Ready to Use!

Everything is live and deployed. Your two-room architecture is ready for real-time collaborative art sessions! 🚀

**Need help?** All files are documented in TWO-ROOM-SETUP.md
