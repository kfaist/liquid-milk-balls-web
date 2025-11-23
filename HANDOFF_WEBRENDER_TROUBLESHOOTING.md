# HANDOFF PROMPT - TouchDesigner WebRender TOP Configuration

## CURRENT OBJECTIVE
Configure TouchDesigner WebRender TOP to receive webcam feeds from any browser globally through LiveKit WebRTC streaming.

## WHAT WE'RE SOLVING
**Problem:** Remote participants (anywhere in world, any browser) need to send their camera feed to TouchDesigner for live processing, then see the processed result back in their browser.

**Current Status:** OUTPUT pipeline (TouchDesigner → NDI → OBS → LiveKit → Remote Viewers) is 100% working.

**What Needs Fixing:** INPUT pipeline (Remote Camera → LiveKit → TouchDesigner)

## SYSTEM ARCHITECTURE

### Complete Pipeline (Goal)
```
Remote Browser (publisher.html)
    ↓
LiveKit Room: "claymation-live"
    ↓
TouchDesigner WebRender TOP (loads td-auto-viewer.html)
    ↓
TouchDesigner Processing
    ↓
NDI Out TOP: "TD-LiveKit-Output"
    ↓
OBS NDI Source
    ↓
OBS WHIP Stream → LiveKit Room: "processed-output"
    ↓
Remote Browser (return-viewer.html) - SHOWS PROCESSED VIDEO
```

### What's Working
- ✅ Node.js server running on localhost:3000 (PID 43492)
- ✅ LiveKit Cloud configured and working
- ✅ OUTPUT pipeline fully operational
- ✅ Remote viewers can see processed video

### What Needs Fixing
- ⚠️ TouchDesigner WebRender TOP at `/webrender_livekit_input` 
- ⚠️ Needs to load `http://localhost:3000/td-auto-viewer.html`
- ⚠️ Must have "Enable Media Stream" turned ON
- ⚠️ Currently shows yellow warning triangle (may or may not be receiving video)

## FILES AND LOCATIONS

### TouchDesigner Project
- **File:** `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\ndi-streamCOPY.toe`
- **Status:** Currently open in TouchDesigner (PID 46996)
- **WebRender Operator:** `/webrender_livekit_input`

### Web Application
- **Directory:** `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web`
- **Server:** Running on http://localhost:3000 (Node.js PID 43492)
- **Key Files:**
  - `td-auto-viewer.html` - LiveKit viewer page that WebRender TOP should load
  - `publisher.html` - Where remote users publish their camera
  - `.env` - Contains LiveKit credentials

### LiveKit Configuration (.env file)
```
LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

### Helper Scripts Created
- `discover_webrender_params.py` - Discovers all WebRender TOP parameters
- `diagnose_webrender_complete.py` - Full diagnostic and configuration script

## WHAT WAS ATTEMPTED IN THIS SESSION

1. **Started systematic troubleshooting** of TouchDesigner WebRender TOP
2. **Created diagnostic scripts** to:
   - Discover WebRender TOP parameter names
   - Configure the WebRender TOP with correct settings
   - Enable media stream access
   - Set correct URL
   - Reload the WebRender TOP
3. **Executed `discover_webrender_params.py`** to enumerate all parameters (process running, output pending)

## CRITICAL INFORMATION FROM DOCUMENTATION

According to the integration guide provided, the WebRender TOP **MUST** have:
1. **"Enable Media Stream" turned ON** - This allows the embedded Chromium browser to use camera/microphone
2. **URL set to:** `http://localhost:3000/td-auto-viewer.html`
3. **Reload pulsed** after changing settings

### Parameter Name Variations
The "Enable Media Stream" setting might be named:
- `Enablemediastream`
- `Enablemedia`  
- `Enableaudio`
- Or some other variation

The `discover_webrender_params.py` script will reveal the exact parameter names.

## NEXT STEPS FOR CONTINUATION

### Step 1: Get Parameter Discovery Results
Check the output from `discover_webrender_params.py` (PID 37460) to see:
- Exact parameter names in this TouchDesigner version
- Current values of all parameters
- Which parameters control media stream access

### Step 2: Configure WebRender TOP
Using the correct parameter names discovered in Step 1:
1. Set URL to `http://localhost:3000/td-auto-viewer.html`
2. Enable media stream parameter (set to True/On)
3. Enable audio parameter if it exists (set to True/On)
4. Pulse the Reload parameter

### Step 3: Verify Configuration
1. Check that WebRender TOP no longer shows yellow warning
2. Open browser to `http://localhost:3000/publisher.html`
3. Click "Start Publishing" to send camera to LiveKit room "claymation-live"
4. Verify that WebRender TOP in TouchDesigner shows the video feed

### Step 4: Test Complete Pipeline
1. Confirm camera feed appears in TouchDesigner WebRender TOP
2. Verify TouchDesigner processing works on the input
3. Confirm NDI output to OBS continues to work
4. Verify remote viewers at `return-viewer.html` see processed video

## ALTERNATIVE APPROACHES (IF WEBRENDER FAILS)

### Fallback Option 1: OBS Virtual Camera Bridge
If WebRender TOP does not work:
1. Have remote user open `publisher.html` in their browser
2. They publish to LiveKit room "claymation-live"
3. Open `td-auto-viewer.html` in a separate browser window
4. Capture that browser window in OBS (Window Capture)
5. Use OBS → NDI → TouchDesigner pipeline
6. This adds latency but guaranteed to work

### Fallback Option 2: Direct NDI from Browser (Requires Plugin)
Not recommended because it requires browser plugin (violates "zero app downloads" requirement)

## IMPORTANT NOTES FOR KRISTA

### Communication Style
- Krista has dyslexia - provide COMPLETE instructions without abbreviations
- Always give full commands, never shortcuts
- Explain each step clearly

### Current System State
- TouchDesigner is OPEN with project loaded
- Node.js server is RUNNING on port 3000
- OBS is OPEN (PID 51784)
- Firefox is OPEN with multiple tabs

### Browser Tabs Currently Open
- Tab 264: http://localhost:3000/publisher.html (publisher page)
- Tab 218: Claude.ai session
- Multiple other research tabs

## SUCCESS CRITERIA

The WebRender TOP configuration will be successful when:
1. ✅ WebRender TOP shows video from remote camera
2. ✅ No yellow warning triangle on WebRender TOP
3. ✅ Remote user can publish camera from any browser
4. ✅ TouchDesigner can process the incoming video
5. ✅ Processed video streams back to remote viewers
6. ✅ Entire pipeline works globally with zero app downloads

## TESTING PROCEDURE

After configuration:
1. Open `http://localhost:3000/publisher.html` in browser
2. Click "Start Publishing"
3. Grant camera permissions
4. Verify video appears in browser
5. Check TouchDesigner WebRender TOP for video
6. Verify complete round-trip works

## FILES TO REFERENCE

- `/mnt/user-data/uploads/ndi-streamCOPY.toe` - TouchDesigner project (copied to Claude's computer)
- Integration guide document (already in context)
- `COMPLETE_HANDOFF_NOVEMBER_22.md` - Previous comprehensive handoff
- `README.md` - Project documentation

## CONTEXT FOR AGENT

This is part of an interactive art installation where:
- Krista Faist is an experimental new media artist
- Work includes "The Mirror's Echo" and preparations for GLEAM 2026
- Critical requirement: global accessibility with zero app downloads
- Uses TouchDesigner for real-time video effects processing
- Currently at 95% completion - just need camera INPUT working

The OUTPUT path is perfect. We just need to get remote cameras INTO TouchDesigner.

---

**Current Session Process Still Running:**
- PID 37460: `discover_webrender_params.py` 
- Status: Executing parameter discovery in TouchDesigner
- Next action: Read the output to get exact parameter names

**Resume by:** Reading process output from PID 37460, then configuring WebRender TOP with discovered parameter names.
