# 📥 COMPLETE INPUT SETUP FOR TOUCHDESIGNER

## The Missing Piece: Getting Video INTO TouchDesigner

You have the OUTPUT working (TD → NDI → OBS → WHIP → LiveKit ✓)

But you need the INPUT configured (Camera → LiveKit → TouchDesigner)

---

## 🎯 The Complete Loop

```
REMOTE CAMERA                    TOUCHDESIGNER              OUTPUT TO VIEWERS
     ↓                                ↓                          ↓
publisher.html            WebRender TOP operator          NDI Out TOP ✓ (you have this!)
     ↓                                ↓                          ↓
LiveKit "claymation-live"   Shows td-auto-viewer.html          OBS ✓ (working!)
     ↓                                ↓                          ↓
td-auto-viewer.html            Your Processing             WHIP Stream ✓ (working!)
  (receives stream)             Effects Here                     ↓
                                     ↓                   LiveKit "processed-output"
                               NDI Out TOP ──────────────────→  return-viewer.html
```

---

## 🔧 IN TOUCHDESIGNER: Add WebRender TOP

### Step 1: Create WebRender TOP Operator

1. **Open TouchDesigner** (your project is already running)

2. **Add a Web Render TOP operator:**
   - Press Tab to open operator menu
   - Type: "webrender" or "web render"
   - Click "Web Render TOP"
   - This creates a browser inside TouchDesigner!

3. **Configure the WebRender TOP:**
   - **URL:** `http://localhost:3000/td-auto-viewer.html`
   - **Active:** ✓ ON (check the box)
   - **Width:** 1920
   - **Height:** 1080
   - **Update Mode:** Realtime

### Step 2: Connect Your Network

```
WebRender TOP (shows camera) 
    ↓
Your Effects (claymation, mirrors, etc.)
    ↓  
NDI Out TOP (already configured ✓)
```

### Step 3: Test the INPUT

1. **Open publisher.html in browser:**
   `http://localhost:3000/publisher.html`

2. **Click "Start Publishing"**
   - Allow camera access
   - You should see yourself in the browser

3. **Look at TouchDesigner WebRender TOP**
   - Should show the same camera feed!
   - This is your INPUT working!

4. **Apply your effects** between WebRender and NDI Out

5. **Your OUTPUT flows:** NDI → OBS → WHIP → LiveKit → Viewer

---

## 🚨 Current Blocker: LiveKit Minutes Exceeded

**You can't test this right now because LiveKit free tier is exhausted.**

**See LIVEKIT_LIMIT_FIX.md for solutions!**

---

## 📋 After You Fix LiveKit Limits

**Test Checklist:**

1. [ ] Open publisher.html → see camera
2. [ ] Click "Start Publishing"
3. [ ] WebRender TOP in TD shows camera feed
4. [ ] Apply your effects
5. [ ] NDI Out sends to OBS
6. [ ] OBS streams via WHIP ✓ (already working!)
7. [ ] return-viewer.html shows processed output

---

## 💡 Why WebRender TOP?

**WebRender TOP is like having a browser inside TouchDesigner:**
- Loads any webpage
- Captures the rendered output
- In this case, loads td-auto-viewer.html which connects to LiveKit
- Shows the camera stream from remote users

**Alternative (more complex):**
- TouchDesigner has experimental WebRTC support
- But WebRender is simpler and more reliable
- Plus it works with your existing web pages!

---

## 🎨 Your Complete Setup

**INPUT PATH:**
- Remote camera → LiveKit → td-auto-viewer.html → WebRender TOP → Effects

**OUTPUT PATH:**  
- Effects → NDI Out → OBS → WHIP → LiveKit → return-viewer.html ✓ WORKING!

**All you're missing:** The WebRender TOP operator in TouchDesigner

**Current blocker:** LiveKit free tier exhausted (fix with LIVEKIT_LIMIT_FIX.md)

---

## Next Steps

1. **Fix LiveKit** (upgrade plan or new project)
2. **Add WebRender TOP** in TouchDesigner with URL: `http://localhost:3000/td-auto-viewer.html`
3. **Connect WebRender** → Your Effects → NDI Out (already exists)
4. **Test complete loop!**

**You're SO close!** Just need LiveKit minutes and the WebRender operator!
