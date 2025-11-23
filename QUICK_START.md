# 🎯 QUICK START GUIDE - Liquid Milk Balls Pipeline

## Daily Startup (3 Steps)

### 1. Start Server
```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
node server.js
```
✓ Server running at http://localhost:3000

### 2. Start TouchDesigner
- Open your project file
- Verify NDI output is active (green indicator)

### 3. Start OBS Streaming
- Launch OBS Studio
- Click "Start Streaming" button
- Look for "LIVE" indicator in bottom right

---

## 🌐 Access Your Pages

**Publisher (Camera Input):**
http://localhost:3000/publisher.html

**Viewer (Processed Output):**
http://localhost:3000/return-viewer.html

**Railway Deployment:**
https://liquid-milk-balls-web-production-2e8c.up.railway.app

---

## ✅ Quick Health Check

| Component | How to Verify |
|-----------|---------------|
| Server | Visit http://localhost:3000 |
| Publisher | See your camera in publisher.html |
| TouchDesigner | NDI output shows green |
| OBS | Status bar shows "LIVE" + upload kbps |
| Viewer | Processed video appears in return-viewer.html |

---

## 🔧 If Something Breaks

**OBS won't stream?**
→ Check: `basic.ini` has correct WHIP settings
→ Run: `node configure_obs_ingress.js`

**No video in viewer?**
→ Check: OBS is streaming (LIVE indicator)
→ Check: TouchDesigner NDI output active

**Server won't start?**
→ Check: Port 3000 not already in use
→ Run: `tasklist | findstr node` to find existing process

---

## 📁 Important Files

**OBS Config:**
`C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\basic.ini`

**Server Code:**
`C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\server.js`

**Automation:**
`C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\automation\START_COMPLETE_PIPELINE.ps1`

---

## 🎨 Your Pipeline at a Glance

```
Camera → LiveKit → TouchDesigner → Effects → NDI → OBS → WHIP → LiveKit → Viewer
         (Input)                                            (Output)
```

**Rooms:**
- claymation-live = camera input
- processed-output = viewer output

---

## 💡 Pro Tips

- Always start components in order: Server → TouchDesigner → OBS
- Wait 3-5 seconds between each startup step
- Check OBS logs if streaming fails (newest file in `%APPDATA%\obs-studio\logs`)
- F5 to refresh browser pages if video doesn't appear
- Keep OBS window visible to monitor stream health

---

**Last Updated:** November 22, 2025
**Status:** ✅ FULLY OPERATIONAL
