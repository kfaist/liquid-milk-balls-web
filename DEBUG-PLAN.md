# 🔍 WebRTC Connection Debugging Plan

## Current Status
- Railway deployment: https://marvelous-blessing-production-4059.up.railway.app/
- Main page: / (publisher with camera)
- Viewer page: /viewer.html (receives video)
- Signaling server: wss://marvelous-blessing-production-4059.up.railway.app/ws

## 🎯 Test Procedure

### Test 1: Check OBS Virtual Camera Detection
**URL:** https://marvelous-blessing-production-4059.up.railway.app/device-test.html

**Steps:**
1. Open device-test.html in Edge/Chrome
2. Click "List All Cameras"
3. Grant camera permission when prompted

**Expected Results:**
- Should show "✅ OBS Virtual Camera DETECTED!" if OBS is running with Virtual Camera started
- Should list all available cameras with their names and IDs

**What to record:**
- [ ] OBS Virtual Camera found? (YES/NO)
- [ ] Camera label shown: _______________
- [ ] Total cameras found: _______________

---

### Test 2: Two-Browser WebRTC Connection Test

**IMPORTANT:** Open these in SEPARATE browser windows (not tabs) side by side

**Browser 1 - Publisher (Main Page):**
URL: https://marvelous-blessing-production-4059.up.railway.app/

**Steps:**
1. Click "Start Camera"
2. Wait for camera preview to show
3. Look at the button states - what buttons are now enabled?
4. Click "Start WebRTC Call"
5. Watch the status text at the bottom

**What to record:**
- [ ] Camera preview shows? (YES/NO)
- [ ] "Start WebRTC Call" button enabled after camera starts? (YES/NO)
- [ ] Status after clicking "Start WebRTC Call": _______________
- [ ] Does status say "Offer sent"? (YES/NO)

**Browser 2 - Viewer:**URL: https://marvelous-blessing-production-4059.up.railway.app/viewer.html

**Steps:**
1. Open this AFTER starting camera in Browser 1
2. Watch the status message at top
3. Wait to see if video appears

**What to record:**
- [ ] Initial status: _______________
- [ ] Does it say "Connected - Waiting for remote camera..."? (YES/NO)
- [ ] Does video appear? (YES/NO)
- [ ] If no video, what does status say? _______________

---

### Test 3: Browser Console Log Check

**Open Developer Tools (F12) in BOTH browsers**

**Browser 1 (Publisher):**
1. Open Console tab
2. Start camera, then start WebRTC call
3. Look for these messages:
   - "Connected to signaling server"
   - "Creating offer..."
   - "Offer sent"
   - Any red error messages?

**What to record:**
- [ ] "Connected to signaling server" appears? (YES/NO)
- [ ] "Offer sent" appears? (YES/NO)
- [ ] Any errors in console? Write them here: _______________

**Browser 2 (Viewer):**
1. Open Console tab
2. Look for these messages:
   - "Connected to signaling server"
   - "Received: offer"
   - "Answer sent"
   - "Received remote track"

**What to record:**
- [ ] "Connected to signaling server" appears? (YES/NO)
- [ ] "Received: offer" appears? (YES/NO)
- [ ] "Received remote track" appears? (YES/NO)
- [ ] Any errors in console? Write them here: _______________
---

### Test 4: Railway Server Logs Check

**Go to Railway Dashboard:**
1. Open https://railway.app
2. Go to your project: liquid-milk-balls-web
3. Click on the deployment
4. Look at the "Logs" tab

**What to look for:**
- "[ws] Client connected" messages (should see 2 when both browsers connect)
- "[ws] Client joined for WebRTC signaling"
- Any error messages?

**What to record:**
- [ ] Server shows client connections? (YES/NO)
- [ ] How many "[ws] Client connected" messages? _______________
- [ ] Any errors in server logs? Write them here: _______________

---

## 🐛 Common Issues & Solutions

### Issue 1: "Start WebRTC Call" button is DISABLED
**Cause:** Camera didn't start properly
**Fix:** 
1. Make sure OBS Virtual Camera is running
2. Refresh page and try "Start Camera" again
3. Check browser permissions (look for camera icon in address bar)

### Issue 2: Viewer says "Connected" but no video
**Possible causes:**
1. Publisher didn't click "Start WebRTC Call"
2. WebSocket signaling failed
3. ICE candidate negotiation failed (firewall/network issue)

**Fix:**
1. Check publisher console for "Offer sent" message
2. Check viewer console for "Received: offer" message
3. Try refreshing BOTH browsers and starting over

### Issue 3: "Connection failed - Check server" in viewer
**Cause:** Can't connect to WebSocket server
**Fix:**
1. Check if Railway deployment is online (https://railway.app)
2. Wait 30 seconds and refresh - Railway may be cold-starting
3. Check Railway logs for errors
---

## 📋 Quick Checklist

Before testing, make sure:
- [ ] OBS is running with Virtual Camera STARTED
- [ ] Railway deployment is online and green
- [ ] Using HTTPS URLs (not HTTP)
- [ ] Using two SEPARATE browser windows (not tabs)
- [ ] Developer Console is open (F12) to see errors

---

## 🚨 If Nothing Works

**Try this emergency test:**

Open ONE browser window with split view:
1. Open https://marvelous-blessing-production-4059.up.railway.app/ (left half)
2. Open https://marvelous-blessing-production-4059.up.railway.app/viewer.html (right half)
3. Start camera on left
4. Start WebRTC call on left
5. Watch right side for video

If this doesn't work, the WebSocket signaling server may not be properly deployed on Railway.

**Check Railway deployment:**
- Go to Settings → Networking
- Make sure port 3000 is exposed
- Check that WebSocket upgrade is enabled

---

## 📝 Notes Section

Use this space to write down what you see during testing:










---

## 🎯 What I Suspect Is Wrong

Based on the code analysis, here's what I think might be happening:

**Most Likely Issue:**
The viewer.html is connecting to the signaling server BEFORE the publisher clicks "Start WebRTC Call". When the viewer connects first, IT becomes the initiator and tries to send an offer, but it has no camera to offer!

**Solution:**
The connection flow should be:
1. Publisher starts camera
2. Publisher clicks "Start WebRTC Call" → becomes initiator
3. Publisher sends offer
4. Viewer opens (or is already open) → receives offer → sends answer

**Try this order:**
1. Main page: Start camera, then immediately click "Start WebRTC Call"
2. THEN open viewer page in second browser
3. Video should appear!

If that doesn't work, come back with your test results and we'll dig deeper!
