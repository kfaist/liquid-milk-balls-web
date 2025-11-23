# ALTERNATIVE INPUT SOLUTION - Using OBS Browser Source

## Problem
WebRender TOP in TouchDesigner has a warning and isn't loading td-auto-viewer.html reliably.

## Better Solution: Use OBS Browser Source

Instead of WebRender TOP → LiveKit, use this path:
```
Camera → LiveKit → OBS Browser Source → NDI → TouchDesigner NDI In TOP
```

This is MORE RELIABLE because:
- OBS Browser Source is battle-tested
- You already have OBS running
- NDI to TouchDesigner already works
- Separates concerns (OBS handles web, TD handles effects)

---

## SETUP STEPS

### Step 1: Add Browser Source in OBS for Input

1. **In OBS, add a new scene** (or use existing)
   - Scene name: "Camera Input from LiveKit"

2. **Add Browser Source:**
   - Sources → Add → Browser
   - Name: "LiveKit Camera Input"
   - URL: `http://localhost:3000/td-auto-viewer.html`
   - Width: 1920
   - Height: 1080
   - ✓ Check "Shutdown source when not visible" OFF
   - ✓ Check "Refresh browser when scene becomes active"
   - Click OK

3. **Enable NDI Output for this scene:**
   - Tools → NDI™ Output Settings
   - Main Output: ON
   - Output Name: "OBS-Input" (or keep as "OBS")

### Step 2: In TouchDesigner - Add NDI In TOP

1. **Add NDI In TOP operator:**
   - Press Tab
   - Type "ndi in" or "ndiin"
   - Create NDI In TOP

2. **Configure NDI In TOP:**
   - Network Source: Select "OBS (Output)" or "OBS-Input"
   - Active: ON
   - Bandwidth: Highest

3. **This NDI In TOP shows the LiveKit camera!**

### Step 3: Connect Your Pipeline

```
NDI In TOP (LiveKit camera)
    ↓
Your Effects Processing
    ↓
NDI Out TOP (already exists - ndiout_livekit2)
    ↓
OBS NDI Source (different scene/instance)
    ↓
WHIP Stream → LiveKit → Viewer
```

---

## Why This Works Better

**WebRender TOP Issues:**
- Chromium rendering engine in TouchDesigner can be finicky
- JavaScript errors harder to debug
- LiveKit WebRTC might have compatibility issues

**OBS Browser Source Advantages:**
- Proven to work (used by thousands of streamers)
- Better Chromium implementation
- Easy to debug (can see in OBS)
- You already have OBS running

---

## Current Status

You have:
- ✓ OBS running
- ✓ Server running on port 3000
- ✓ LiveKit upgraded to paid
- ✓ NDI Out working (OBS streams to LiveKit successfully)

You need:
- [ ] OBS Browser Source for camera INPUT
- [ ] TouchDesigner NDI In TOP for that input
- [ ] Connect NDI In → Effects → NDI Out

---

## Next Steps

I'll create an automated script to configure this for you...
