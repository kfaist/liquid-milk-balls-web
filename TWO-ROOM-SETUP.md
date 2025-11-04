# 🎨 The Mirror's Echo - Two-Room Architecture

## ✅ What's Built

**Two-room bidirectional streaming system:**
- Remote participants see your processed output (BIG with popout)
- You receive their camera input for processing
- Clean, beautiful UI matching your site design

---

## 🏗️ Architecture

```
REMOTE PARTICIPANT                    KRISTA (YOU)
   webcam ──────> input-room ──────> your studio
                                         │
                                     OBS/TD process
                                         │
   display <───── output-room <───── td-publisher
```

---

## 📄 Three New Pages

### 1. **remote-participant.html** (for viewers)
**URL:** https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html

- **LEFT (BIG):** Your processed output with breathing popout button ⤢
- **RIGHT (small):** Their webcam preview
- Click "Start Camera" to begin
- Publishes to input-room, receives from output-room

### 2. **krista-studio.html** (your control room)
**URL:** http://localhost:3000/krista-studio.html

- **LEFT:** Receives their input (with popout for focusing)
- **RIGHT:** Preview of your local camera
- Auto-connects to input-room
- Shows when participant joins

### 3. **td-publisher.html** (your broadcast tool)
**URL:** http://localhost:3000/td-publisher.html

- Publishes OBS Virtual Camera to output-room
- Use this to send processed video back to participants

---

## 🎯 Complete Workflow

### Setup (You):
1. Open **krista-studio.html** - monitor incoming participant
2. Start OBS → Virtual Camera
3. Open **td-publisher.html** → "Start OBS Virtual Camera" → "Publish to Railway"
4. Send participant the Railway URL

### Participant Flow:
1. Opens: https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html
2. Clicks "Start Camera" (allows webcam)
3. Their camera feeds to YOU
4. They see YOUR processed output (big, beautiful, with popout)

### Your Processing:
```
Their camera (krista-studio.html left panel)
    ↓
OBS captures input
    ↓
NDI → TouchDesigner (your effects)
    ↓
NDI back to OBS
    ↓
Virtual Camera → td-publisher.html → output-room
    ↓
Participant sees result (remote-participant.html left panel)
```

---

## 🚀 Deploy to Railway

**Current server running:** http://localhost:3000 (PID 33492)

**To deploy:**
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add .
git commit -m "Add two-room bidirectional streaming"
git push
```

Railway auto-deploys in ~2 minutes.

**Live URLs after deploy:**
- Participant page: https://marvelous-blessing-production-4059.up.railway.app/remote-participant.html
- Your studio: https://marvelous-blessing-production-4059.up.railway.app/krista-studio.html
- Publisher: https://marvelous-blessing-production-4059.up.railway.app/td-publisher.html

---

## 🎨 Features

**Remote Participant Experience:**
- ✅ Beautiful design matching your site
- ✅ Big display of your processed art
- ✅ Breathing popout button (⤢) top-left
- ✅ Fullscreen overlay with "Pop Out to Window" button
- ✅ Small webcam preview (top-right)
- ✅ Auto-reconnect if disconnected

**Your Studio Control:**
- ✅ Live monitoring of participant input
- ✅ Popout button to focus on their camera
- ✅ Preview of your local camera
- ✅ Status indicators for all connections

**Technical:**
- ✅ Room-based WebRTC signaling
- ✅ Low-latency streaming
- ✅ Auto-reconnect logic
- ✅ No FFmpeg or LiveKit dependencies
- ✅ Clean error handling

---

## 🛑 Stop/Restart Server

**Stop:**
```bash
Ctrl+C
```

**Restart:**
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
npm start
```

---

## 📝 Files Changed/Created

**New:**
- `remote-participant.html` - Beautiful viewer page
- `krista-studio.html` - Your control room
- `server.js` - Updated with room support

**Unchanged:**
- `index.html` - Original Mirror's Echo site
- `td-publisher.html` - OBS broadcaster
- `split-viewer.html` - Old split view (still works)

---

## ✨ Ready to Test

1. **Local test first:**
   - Open http://localhost:3000/krista-studio.html
   - Open http://localhost:3000/remote-participant.html in another tab
   - Click "Start Camera" on participant page
   - You should see their camera in your studio

2. **Then add OBS/TD:**
   - Open http://localhost:3000/td-publisher.html
   - Start OBS Virtual Camera
   - Click "Publish to Railway"
   - Participant should see your processed output

3. **Deploy when ready:**
   - `git push` to Railway
   - Share Railway URL with remote participants

---

**Ready to go! 🚀**
