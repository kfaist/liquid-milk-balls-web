# 🧪 COMPLETE TESTING GUIDE - WebRTC Bidirectional Streaming

## ✅ Current Status Check

**Server**: Running on http://localhost:3000 ✅
**TouchDesigner**: Open with ndi-streamCOPY.toe ✅  
**OBS Studio**: Running ✅
**Your IP**: 192.168.24.70 ✅

**Browser Pages Opened**:
- Publisher: http://192.168.24.70:3000/publisher.html
- Auto Viewer: http://localhost:3000/td-auto-viewer.html
- Control Center: http://localhost:3000/control-center.html

---

## 🎯 STEP-BY-STEP TESTING PROCEDURE

### STEP 1: Set Up TouchDesigner (2 minutes)

1. **In TouchDesigner, press Alt+T** (opens Textport)

2. **Copy this ENTIRE command** (select all, Ctrl+C):
   ```python
   exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_auto_setup.py').read())
   ```

3. **Paste into Textport** (right-click or Ctrl+V) and press Enter

4. **You should see**:
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║  TouchDesigner WebRTC/LiveKit Auto-Setup                  ║
   ╚════════════════════════════════════════════════════════════╝
   
   SETTING UP WEBRTC RECEIVER
   ✅ Created: /webrender_livekit_input
   
   SETTING UP NDI OUTPUT  
   ✅ Found existing NDI Out (or created new one)
   
   SETUP COMPLETE!
   ```

5. **Check your network**:
   - You should see a new operator: `webrender_livekit_input`
   - It should show the webpage loading
   - NDI Out should be active

---

### STEP 2: Test Publisher (Phone or Browser)

**Option A: Same Computer (Quick Test)**

1. In the browser tab that opened (publisher.html):
   - Click **"Start Publishing"**
   - Grant camera/microphone permissions
   - You should see yourself in the preview

2. Check the status shows "Connected"

**Option B: Your Phone (Real Test)**

1. On your phone (connected to same WiFi):
   - Open browser
   - Go to: **http://192.168.24.70:3000/publisher.html**
   - Click "Start Publishing"
   - Grant permissions
   - You should see yourself

---

### STEP 3: Verify TouchDesigner Receives Video

1. **Look at the `webrender_livekit_input` operator** in TouchDesigner

2. **You should see**:
   - The webpage interface initially
   - Status: "CONNECTING..." then "CONNECTED"
   - Then: "RECEIVING: publisher-xxxxx"
   - **YOUR VIDEO should appear fullscreen!**

3. **If you see black screen**:
   - Right-click the Web Render TOP → Set Active to OFF
   - Wait 2 seconds
   - Set Active to ON
   - The page should reload

4. **If you see "WAITING FOR STREAM"**:
   - Publisher hasn't started yet
   - Make sure you clicked "Start Publishing"
   - Check camera permissions were granted

---

### STEP 4: Verify NDI Output

1. **In TouchDesigner**:
   - Look at your NDI Out TOP
   - Parameter "Active" should be ON
   - Parameter "NDI Name" should be "TD-LiveKit-Output"

2. **The NDI Out should show the same video** as Web Render
   (Because they're directly connected for testing)

---

### STEP 5: Set Up OBS to Capture

1. **In OBS Studio**:
   - Click **+ (Add Source)**
   - Select **NDI™ Source**

2. **In the NDI Source settings**:
   - Source Name: Select **"YOUR-COMPUTER (TD-LiveKit-Output)"**
   - Bandwidth: Highest
   - Click OK

3. **You should see your video** in OBS!

4. **Resize/position** the NDI source in your scene

---

### STEP 6: Configure OBS WHIP Output (If Not Already Done)

1. **In OBS**: Settings → Stream

2. **Service**: Select "WHIP"

3. **Get WHIP URL**:
   - Open: http://localhost:3000/api/processed-publisher-token
   - Copy the `whipUrl` value (entire URL including token)

4. **In OBS Stream settings**:
   - Server: Paste the whipUrl
   - Bearer Token: Leave empty
   - Click Apply, then OK

5. **Start Streaming** in OBS

---

### STEP 7: Test Viewer Receives Processed Output

1. **On your phone or browser**:
   - Open: **http://192.168.24.70:3000/return-viewer.html**
   - Click **"Join Stream"**

2. **You should see**:
   - The video from TouchDesigner
   - Currently it's just a passthrough
   - But it proves the complete loop works!

---

## ✅ COMPLETE LOOP VERIFICATION

If everything is working, you should see:

1. **Phone Camera** → LiveKit → **TouchDesigner Web Render**  ✅
2. **TouchDesigner** → **NDI Out** → **OBS** ✅
3. **OBS** → WHIP → **LiveKit** → **Return Viewer** ✅

**COMPLETE BIDIRECTIONAL LOOP WORKING!** 🎉

---

## 🎨 NEXT: Add Your Processing

Once the loop is verified:

1. **In TouchDesigner**:
   - Select the NDI Out TOP
   - Right-click the input connector
   - Click "Disconnect"

2. **Insert your effects**:
   - Add your liquid milk balls effects
   - Color manipulation
   - Whatever processing you want!

3. **Connect the chain**:
   - Web Render → Your Effects → NDI Out

4. **Test again**:
   - Remote viewer should now see processed video!

---

## 🐛 TROUBLESHOOTING

### Web Render shows nothing
```
Solution:
1. Check URL is correct: http://localhost:3000/td-auto-viewer.html
2. Set Active OFF then ON
3. Check server is running: http://localhost:3000/healthz
```

### "WAITING FOR STREAM" in Web Render
```
Solution:
1. Publisher hasn't started
2. Make sure you clicked "Start Publishing"  
3. Check camera permissions granted
4. Verify you're in the same room (claymation-live)
```

### OBS doesn't see NDI source
```
Solution:
1. Make sure NDI Out is Active in TouchDesigner
2. Check NDI Name is "TD-LiveKit-Output"
3. Restart OBS
4. Both TouchDesigner and OBS need same privilege level
```

### Return viewer shows black
```
Solution:
1. Make sure OBS is streaming (check "Live" indicator)
2. Verify WHIP is configured correctly
3. Check OBS scene has NDI source visible
4. Refresh return-viewer page
```

---

## 📊 TESTING CHECKLIST

Use this to track your progress:

- [ ] TouchDesigner setup script executed successfully
- [ ] webrender_livekit_input operator created
- [ ] NDI Out TOP active and configured
- [ ] Publisher page opened and camera started
- [ ] TouchDesigner shows remote video
- [ ] OBS NDI source added and shows video
- [ ] OBS WHIP configured with LiveKit URL
- [ ] OBS streaming started
- [ ] Return viewer receives processed output
- [ ] Complete loop verified!

---

## 🎉 SUCCESS CRITERIA

You'll know everything is working when:

1. ✅ You see your phone camera in TouchDesigner
2. ✅ OBS shows the same video from NDI
3. ✅ Return viewer shows the video from OBS
4. ✅ Less than 1-2 second delay end-to-end
5. ✅ Audio is present (if enabled)

---

## 📱 URLs FOR REMOTE TESTING

**Publisher** (send camera TO you):
```
http://192.168.24.70:3000/publisher.html
```

**Viewer** (receive processed video FROM you):
```
http://192.168.24.70:3000/return-viewer.html
```

**Control Center** (all links):
```
http://localhost:3000/control-center.html
```

---

## 🚀 WHEN READY TO GO LIVE

Deploy to Railway for internet access:

```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add .
git commit -m "Add TouchDesigner WebRTC bidirectional streaming - TESTED AND WORKING"
git push
```

Then share these URLs globally:
- Publisher: https://marvelous-blessing-production-4059.up.railway.app/publisher.html
- Viewer: https://marvelous-blessing-production-4059.up.railway.app/return-viewer.html

---

## ✨ You're Ready!

Test each step carefully, and you'll have a complete bidirectional WebRTC streaming system working through TouchDesigner!

**Start with STEP 1 above!** 🎯
