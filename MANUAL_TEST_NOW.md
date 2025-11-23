# ⚡ MANUAL TEST GUIDE - 3 MINUTES

## YOU HAVE EVERYTHING OPEN - JUST FOLLOW THESE STEPS!

**Status Right Now:**
- ✅ Node server running (PID 43492, started yesterday)
- ✅ Publisher.html open in Firefox (Tab 60)
- ✅ td-auto-viewer.html open in Firefox (Tab 61)
- ✅ Fix deployed (LiveKit SDK v2.0.7)

---

## 🎬 STEP 1: Start Camera in Publisher (30 seconds)

1. **Go to Firefox Tab 60** - should say "Publisher — The Mirror's Echo"
2. **Click the "Start Camera" button** (big button on the page)
3. **Grant camera permissions** if browser asks
4. **✅ Success when:** You see yourself on the page

---

## 🎬 STEP 2: Check Viewer Console (1 minute)

1. **Go to Firefox Tab 61** - should say "TouchDesigner Auto Viewer - LiveKit Input"
2. **Press F12 key** to open Developer Tools
3. **Click "Console" tab** at the top of Developer Tools
4. **Look for these messages in the console:**

```
[TD-VIEWER] Fetching token...
[TD-VIEWER] Connecting...
[TD-VIEWER] Connected: claymation-live
[TD-VIEWER] Video from: [participant-name]
```

5. **✅ Success when:**
   - Status in top-left corner says "Connected: claymation-live" (in green)
   - You see video from publisher on the page
   - Console shows "Video from:" message

---

## 🎬 STEP 3: Check TouchDesigner (1 minute)

1. **Open TouchDesigner** (or switch to it if already open)
2. **Find the webrender operator** named `webrender_livekit_input`
3. **Look at the operator's display window**

**✅ SUCCESS = You see camera video inside the operator!**

### If webrender shows black or doesn't show video:

**Option A: Reload via Textport** (recommended)

1. In TouchDesigner, press **Alt+T** to open Textport
2. Paste this command and press Enter:

```python
op('/webrender_livekit_input').par.url = 'http://localhost:3000/td-auto-viewer.html'
op('/webrender_livekit_input').par.active = True
op('/webrender_livekit_input').par.reload.pulse()
print("✓ RELOADED")
```

3. Check if video appears

**Option B: Reload via Parameter Panel**

1. Click on the `webrender_livekit_input` operator
2. In parameter panel, find "URL" parameter
3. Make sure it says: `http://localhost:3000/td-auto-viewer.html`
4. Find "Reload" parameter
5. Click the "Pulse" button next to it

---

## 🎯 WHAT YOU SHOULD SEE

### In Publisher (Tab 60):
- Your camera video playing
- Status showing "Connected"

### In td-auto-viewer (Tab 61):
- Status in green: "Connected: claymation-live"
- Your camera video playing (same as publisher)
- Console showing connection messages

### In TouchDesigner:
- webrender operator showing your camera video
- Same video as in the browser tabs

---

## 🐛 TROUBLESHOOTING

### Problem: Publisher doesn't start camera

**Solution:** Refresh the page and try again. Make sure camera isn't being used by another application.

### Problem: td-auto-viewer shows "Connecting..." forever

**Solutions:**
1. Check publisher is actually streaming (should see yourself)
2. Refresh td-auto-viewer page (F5)
3. Check console for errors (F12)
4. Verify Node server is running: Open PowerShell and run:
   ```powershell
   Get-Process -Id 43492
   ```

### Problem: TouchDesigner shows black

**Solutions:**
1. Reload webrender (use Textport command above)
2. Check webrender URL parameter is correct
3. Make sure webrender "active" parameter is ON
4. Check that browser pages are working first

---

## 📊 YOUR COMPLETE PIPELINE

```
Camera
  ↓
publisher.html (Tab 60)
  ↓
LiveKit Cloud (room: claymation-live)
  ↓
td-auto-viewer.html (Tab 61) ← YOU ARE TESTING THIS
  ↓
TouchDesigner webrender ← CHECK THIS NEXT
  ↓
NDI Output
  ↓
OBS
  ↓
LiveKit Cloud (room: processed-output)
  ↓
return-viewer.html
```

**Current Test:** Making sure video flows from publisher → td-auto-viewer → TouchDesigner

---

## ✅ SUCCESS CRITERIA

**Pipeline is 100% working when:**

1. ✅ Publisher shows your camera
2. ✅ td-auto-viewer shows your camera
3. ✅ td-auto-viewer console shows "Connected" and "Video from:"
4. ✅ TouchDesigner webrender shows your camera
5. ✅ No errors in browser console

**When you see all 5: PIPELINE COMPLETE! 🎉**

---

## 💡 WHAT THE FIX DID

**Before:** Used unpinned LiveKit SDK from unpkg.com
- Could load any version
- Sometimes loaded incompatible versions
- Video subscription failed randomly

**After:** Pinned LiveKit SDK to v2.0.7 from jsdelivr.com
- Always loads same version
- Guaranteed compatible API
- Reliable video subscription

**This is line 53 in td-auto-viewer.html:**
```html
<script src="https://cdn.jsdelivr.net/npm/livekit-client@2.0.7/..."></script>
```

---

**Test Time:** 3 minutes  
**Difficulty:** Easy - just follow the steps!  
**Result:** You'll see if the fix works! 🎬
