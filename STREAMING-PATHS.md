# 🎥 COMPLETE STREAMING PATH REFERENCE

## 📊 YOUR LIVEKIT ROOMS

**INPUT ROOM:** `claymation-live` (or whatever you set in LIVEKIT_ROOM_NAME)
- Remote camera publishes here
- OBS Browser Source views this

**PROCESSED ROOM:** `processed-output` (or whatever you set in LIVEKIT_PROCESSED_ROOM)
- OBS WHIP output publishes here (after TouchDesigner processing)
- Return viewer watches this

---

## 🔗 STREAMING ENDPOINTS

### **1. Remote Camera → LiveKit (Input Room)**

**Remote user opens:** https://marvelous-blessing-production-4059.up.railway.app/publisher.html

**What it does:**
- Fetches token from: `/api/publisher-token`
- Publishes webcam to room: `claymation-live`

**Token includes:**
- Room name: `claymation-live`
- Permissions: Can publish + subscribe
- TTL: 2 hours

---

### **2. OBS Browser Source → View Input (For Capture)**

**OBS Browser Source URL:** https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html

**What it does:**
- Fetches token from: `/api/viewer-token`
- Subscribes to room: `claymation-live`
- Shows remote camera feed

**OBS Setup:**
1. Add "Browser" source
2. URL: https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html
3. Width: 1920, Height: 1080
4. Check "Shutdown source when not visible"

---

### **3. OBS → TouchDesigner (NDI)**

**In OBS:**
1. Tools → NDI Output Settings
2. Check "Main Output"
3. Output Name: "OBS" (or whatever you want)

**In TouchDesigner:**
1. Add NDI In TOP
2. Device: Select "OBS (DESKTOP-...)"
3. Now you can process the video!

---

### **4. TouchDesigner → OBS (NDI Return)**

**In TouchDesigner:**
1. Add NDI Out TOP
2. Connect your processed video to it
3. NDI Name: "TouchDesigner-Output" (or whatever)

**In OBS (New Scene):**
1. Add Source → NDI Source
2. Source Name: Select "TouchDesigner-Output"
3. This is your processed video!

---

### **5. OBS → LiveKit (WHIP Streaming)**

**🚨 THIS IS THE CRITICAL PART FOR STREAMING BACK TO LIVEKIT**

**To get your WHIP URL:**

Option A - Fetch it programmatically:
```
Open: https://marvelous-blessing-production-4059.up.railway.app/api/processed-publisher-token
```

You'll see JSON like:
```json
{
  "token": "eyJhbGciOiJS...",
  "url": "wss://your-livekit-server.com",
  "room": "processed-output",
  "whipUrl": "https://your-livekit-server.com/whip?access_token=eyJhbGciOiJS..."
}
```

Copy the **whipUrl** value!

Option B - I'll create a helper page for you (see below)

---

### **OBS WHIP CONFIGURATION:**

**In OBS:**
1. Settings → Stream
2. Service: WHIP
3. Server: (paste the whipUrl from above)
4. Bearer Token: (leave EMPTY - token is in URL)
5. Click OK
6. Click "Start Streaming"

**IMPORTANT:** 
- The URL already includes the access token as a query parameter
- Do NOT put anything in Bearer Token field
- The stream goes to LiveKit room: `processed-output`

---

### **6. Remote Viewer → Watch Processed Video**

**Remote user opens:** https://marvelous-blessing-production-4059.up.railway.app/return-viewer.html

**What it does:**
- Fetches token from: `/api/processed-viewer-token`
- Subscribes to room: `processed-output`
- Shows the processed video from OBS

---

## 🎯 COMPLETE SIGNAL FLOW

```
1. Remote Camera (publisher.html)
   ↓ [publishes to LiveKit]
   
2. LiveKit Room: "claymation-live"
   ↓ [OBS Browser Source views]
   
3. OBS (Captures browser source)
   ↓ [NDI Output]
   
4. TouchDesigner (NDI In)
   ↓ [Process, add effects, etc.]
   
5. TouchDesigner (NDI Out)
   ↓ [NDI Return]
   
6. OBS (NDI Source + WHIP Stream)
   ↓ [Streams to LiveKit via WHIP]
   
7. LiveKit Room: "processed-output"
   ↓ [Remote viewer subscribes]
   
8. Return Viewer (return-viewer.html)
   ✅ Shows final processed video!
```

---

## 🔑 QUICK REFERENCE - URLS YOU NEED

**For Remote Camera:**
`https://marvelous-blessing-production-4059.up.railway.app/publisher.html`

**For OBS Browser Source:**
`https://marvelous-blessing-production-4059.up.railway.app/ndi-viewer.html`

**For OBS WHIP URL:**
`https://marvelous-blessing-production-4059.up.railway.app/api/processed-publisher-token`
(Copy the "whipUrl" from the JSON response)

**For Remote Viewer:**
`https://marvelous-blessing-production-4059.up.railway.app/return-viewer.html`

---

## 🐛 TROUBLESHOOTING

**If remote camera not showing in OBS Browser Source:**
- Check Railway logs for LiveKit connection
- Make sure publisher.html is open and connected
- Refresh OBS browser source

**If TouchDesigner not receiving NDI:**
- Check OBS → Tools → NDI Output Settings is enabled
- Make sure NDI In TOP device is set correctly
- Try refreshing the NDI device list

**If OBS WHIP stream fails:**
- Verify WHIP URL includes access token
- Check LiveKit server is accessible
- Look at OBS → View → Stats for connection errors
- Make sure Bearer Token field is EMPTY

**If return-viewer shows nothing:**
- Verify OBS is streaming (green "Stop Streaming" button)
- Check Railway logs for LiveKit connections
- Make sure processed-output room has active publishers
