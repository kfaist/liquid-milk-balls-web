# 🎯 COMPLETE TEST PLAN - After OBS Fix

## ✅ WHAT I FIXED:
Changed your OBS WHIP URL from the WRONG room to the CORRECT room:
- ❌ OLD: `claymation-live` (input room - where remote cameras publish)
- ✅ NEW: `processed-output` (output room - where viewers watch)

**File modified:** `C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\basic.ini`

---

## 📋 TESTING STEPS:

### Step 1: Restart OBS (REQUIRED!)
1. **Close OBS completely** (File → Exit)
2. **Reopen OBS Studio**
3. **Verify the fix:** Settings → Stream → Should show the new WHIP URL

---

### Step 2: Add TouchDesigner NDI Source (if not already)
**In OBS:**
1. Sources → Add → **NDI Source**
2. Source Name: **"KRISTA-SHOWPUTER-01 (TouchDesigner)"** or **"Touchdesigner"**
3. Your processed video should appear in OBS preview

---

### Step 3: Start Streaming
**In OBS:**
1. Click **"Start Streaming"** button
2. Button should turn green and say **"Stop Streaming"**
3. Watch the bottom status bar:
   - Should show upload KB/s
   - Should show FPS (30fps)
   - Should show "LIVE" indicator

---

### Step 4: Test the Output
**Open this URL in your browser:**
```
https://marvelous-blessing-production-4059.up.railway.app/return-viewer.html
```

**What you should see:**
- ✅ Green status: "Connected - Waiting for remote camera..." changes to "Receiving video!"
- ✅ Your TouchDesigner processed video appears in fullscreen
- ✅ Video is smooth and real-time

---

### Step 5: Test the Complete Loop
**Open a second browser (or use your phone):**
```
https://marvelous-blessing-production-4059.up.railway.app/publisher.html
```

1. Click "Start Camera"
2. Allow camera permission
3. Should say "Connected to LiveKit"

**Back in TouchDesigner:**
- Your NDI In should now show the remote camera!
- Process it, send to NDI Out
- OBS captures it and streams it back
- return-viewer.html shows the processed result!

---

## 🎯 FULL SIGNAL FLOW:

```
Remote Camera (publisher.html)
    ↓ [LiveKit: claymation-live]
OBS Browser Source (ndi-viewer.html)
    ↓ [NDI Output]
TouchDesigner NDI In
    ↓ [Your Processing/Effects]
TouchDesigner NDI Out
    ↓ [NDI]
OBS NDI Source
    ↓ [WHIP Stream - FIXED!]
LiveKit: processed-output ← CORRECT ROOM NOW!
    ↓
Return Viewer (return-viewer.html)
    ✅ Shows processed video!
```

---

## 🚨 TROUBLESHOOTING:

**If OBS won't start streaming:**
- Check Settings → Output → Streaming
- Make sure encoder is set (NVENC recommended)
- Check your internet connection

**If return-viewer shows nothing:**
- Make sure OBS is actually streaming (green button)
- Check OBS stats at bottom for upload activity
- Refresh the return-viewer.html page

**If you see "Connection failed":**
- Token might have expired (valid 24 hours)
- Get new token: https://marvelous-blessing-production-4059.up.railway.app/api/processed-publisher-token
- Update OBS Settings → Stream → Server URL

---

## 📊 HOW TO VERIFY IT'S WORKING:

**OBS indicators:**
- [x] "Stop Streaming" button is green
- [x] Bottom bar shows: "LIVE  |  00:00:00  |  KB/s: 2500+  |  FPS: 30"
- [x] No red connection errors

**Browser indicators:**
- [x] return-viewer.html shows video
- [x] Video is smooth, not frozen
- [x] Status says "Live!" or "Connected"

---

## 🎉 SUCCESS CRITERIA:

You'll know it's working when:
1. ✅ OBS shows active stream stats
2. ✅ return-viewer.html shows your processed video
3. ✅ Video plays in real-time with no major lag
4. ✅ You can open multiple return-viewer tabs and all show the same stream

---

## 📝 NOTES:

**Token expiration:** Your WHIP token expires in ~24 hours. When it expires:
1. Open: https://marvelous-blessing-production-4059.up.railway.app/api/processed-publisher-token
2. Copy the new `whipUrl` value
3. Update OBS Settings → Stream → Server

**If you change the token, you DON'T need to restart OBS** - just stop and start streaming again.

---

**NOW GO TEST IT!** 🚀
