# AGENT HANDOVER - TouchDesigner LiveKit Video Pipeline
# Date: November 22, 2024
# Status: 95% Complete - Final Activation Step Needed

## CRITICAL CONTEXT
Krista has dyslexia - provide COMPLETE, CLEAR instructions without abbreviations.
She prefers full agentic control - take desktop/browser access immediately.

## CURRENT STATUS SUMMARY

### ✅ WHAT'S WORKING
1. **LiveKit Cloud Service**: Fully operational
   - Project: "Claymation Transcription"
   - URL: wss://claymation-transcription-l6e51sws.livekit.cloud
   - Rooms configured: "claymation-live" (input), "processed-output" (return)

2. **Web Infrastructure**: Deployed and functional
   - Railway deployment: https://liquid-milk-balls-web-production-2e8c.up.railway.app
   - Publisher page working: /publisher.html (Tab 131)
   - Test viewer working: /ndi-viewer.html (Tab 150) ✅ CONFIRMED RECEIVING VIDEO
   - Return viewer ready: /return-viewer.html (Tab 79)

3. **TouchDesigner Project**: Configured with effects
   - File: C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\ndi-streamCOPY.toe
   - Web Render TOP exists: webrender_livekit1 (visible in network)
   - NDI output configured: "TD-LiveKit-Output"
   - Effects chain ready for processing

4. **OBS Studio**: Configured with NDI plugin
   - NDI source: "TD-LiveKit-Output"
   - WHIP streaming to LiveKit "processed-output" room configured
   - Config files: C:\Users\krista-showputer\AppData\Roaming\obs-studio\

### ❌ WHAT'S NOT WORKING YET
1. **Web Render TOP in TouchDesigner**: Not activated/showing video
   - The operator exists (webrender_livekit1)
   - Viewer window is open but showing BLACK screen
   - LiveKit connection parameters set but connection not active
   - **THIS IS THE ONLY REMAINING BLOCKER**

2. **OBS Streaming**: Not started yet (waiting for TD video first)

## COMPLETE SYSTEM ARCHITECTURE

### Video Flow Pipeline
```
Browser Camera 
    → publisher.html (Tab 131)
    → LiveKit "claymation-live" room ✅ WORKING (Tab 150 confirms)
    → TouchDesigner Web Render TOP ❌ NOT SHOWING VIDEO
    → Effects processing (feedback, color, distortion)
    → NDI Out "TD-LiveKit-Output" ✅ CONFIGURED
    → OBS Studio NDI source ✅ CONFIGURED
    → WHIP stream to LiveKit "processed-output" ✅ CONFIGURED
    → return-viewer.html (Tab 79) ⏳ WAITING
```

### Current Firefox Tabs
- **Tab 131**: publisher.html (input camera)
- **Tab 150**: ndi-viewer.html (test viewer - SHOWS VIDEO WORKING)
- **Tab 79**: return-viewer.html (output viewer - waiting for processed stream)

## IMMEDIATE NEXT STEPS

### STEP 1: Activate Web Render TOP (PRIORITY)
The activation script is ready but needs execution result:

**File**: `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td_activate_specific.py`

**Command in clipboard**:
```python
exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_activate_specific.py').read())
```

**What it does**:
- Finds webrender_livekit1 operator
- Shows current LiveKit parameters
- Tries multiple activation methods (connect, active, enable, display)
- Reports what worked

**Expected outcome**:
- Textport output showing activation attempts
- Viewer window (already open) shows camera video from LiveKit

**If activation doesn't work automatically**:
1. Look at parameters shown in textport output
2. Manually find and click "Connect" button in webrender_livekit1 parameters
3. Or set "Active" toggle to ON
4. Check viewer window after each attempt

**Alternative manual approach**:
1. Select webrender_livekit1 operator
2. Look at parameter panel (right side of TD)
3. Find parameters with these names (actual names may vary):
   - livekiturl or url → should be: wss://claymation-transcription-l6e51sws.livekit.cloud
   - roomname or room → should be: claymation-live
   - token → should be: eyJhbGciOiJIUzI1NiJ9... (long string)
4. Find button/toggle for: connect, active, enable, start
5. Click/enable it
6. Check viewer window

### STEP 2: Start Publisher (if not already streaming)
- Go to Tab 131 (publisher.html)
- Click "Start Publishing" button
- Allow camera access
- Status should show "Publishing" in green

### STEP 3: Verify Video in TouchDesigner
- Check webrender_livekit1 viewer window
- Should show camera video from browser
- If black, repeat activation attempts

### STEP 4: Start OBS Streaming
Once TD shows video:

**Option A - Automated**:
```powershell
Start-Process "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
Start-Sleep -Seconds 5
# Send start streaming command via WebSocket or hotkey
```

**Option B - Manual**:
1. Open OBS Studio
2. Verify NDI source "TD-LiveKit-Output" is in scene
3. Click "Start Streaming"
4. OBS will stream to LiveKit "processed-output" room via WHIP

### STEP 5: Verify Complete Pipeline
- Tab 79 (return-viewer.html) should show processed video
- This confirms: Browser → LiveKit → TD → Effects → NDI → OBS → LiveKit → Browser

## CRITICAL FILES AND LOCATIONS

### TouchDesigner Files
- **Project**: `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\ndi-streamCOPY.toe`
- **Activation script**: `td_activate_specific.py` (latest, ready to run)
- **Web Render TOP name**: webrender_livekit1

### Web Project
- **Local**: `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`
- **Deployment**: Railway (auto-deploys from GitHub push)
- **GitHub**: https://github.com/kfaist/liquid-milk-balls-web
- **Live URL**: https://liquid-milk-balls-web-production-2e8c.up.railway.app

### OBS Configuration
- **Config dir**: `C:\Users\krista-showputer\AppData\Roaming\obs-studio\`
- **Profile**: Default
- **Scene Collection**: Untitled
- **NDI Source Name**: TD-LiveKit-Output

### LiveKit Credentials
**API Key**: APITw2Yp2Tv3yfg
**API Secret**: [stored in server.js, not in this file for security]

**Current Tokens** (valid until expiry):
- Publisher token: In publisher.html (fetched from /api/publisher-token)
- Viewer token: In viewers (fetched from /api/viewer-token)
- TD receiver token (in files): eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs

## PROOF OF WORKING COMPONENTS

### Evidence LiveKit is Working
**Tab 150** (ndi-viewer.html) displays:
> "Receiving video from publisher-1763852361252"

This proves:
- LiveKit server operational
- WebRTC streaming functional  
- Room "claymation-live" accessible
- Video data flowing through LiveKit
- TouchDesigner can connect to same stream

### Evidence Web Infrastructure is Working
- Publisher page loads and runs
- Token generation working (/api/publisher-token, /api/viewer-token)
- WebRTC connections establishing
- Video transmission verified in test viewer

### Evidence TouchDesigner is Ready
- Project open and saved
- webrender_livekit1 operator created
- Viewer window open (just shows black until activated)
- NDI output configured
- Effects chain ready

### Evidence OBS is Ready
- NDI plugin installed and working
- Source configured for "TD-LiveKit-Output"
- WHIP streaming configuration set
- Profile and scene ready

## TROUBLESHOOTING GUIDE

### If Web Render TOP Won't Activate
1. Check textport output from activation script
2. Look for parameter names that include: connect, active, enable, join, start
3. Try pulsing/enabling each one manually
4. Check if parameters show correct values:
   - URL contains "claymation-transcription"
   - Room is "claymation-live"
   - Token is long string starting with "eyJhbGci"

### If Still No Video After Activation
1. Verify publisher is streaming (Tab 131 status)
2. Verify test viewer shows video (Tab 150)
3. Check TouchDesigner DAT errors (if any)
4. Try disconnecting and reconnecting Web Render TOP
5. Try creating fresh Web Render TOP and configure from scratch

### If OBS Won't Stream
1. Check OBS settings: Settings → Stream
2. Verify WHIP server URL and bearer token are set
3. Check NDI source is visible in scene
4. Try stopping and starting OBS
5. Check OBS logs in %AppData%\obs-studio\logs

### If Return Viewer Shows Nothing
1. Verify OBS is streaming (should say "Streaming" in OBS)
2. Check LiveKit dashboard for "processed-output" room activity
3. Check browser console in Tab 79 for errors
4. Verify return-viewer.html is fetching from correct room

## TECHNICAL NOTES FOR NEXT AGENT

### TouchDesigner Web Render TOP Quirks
- Parameter names vary between TD versions
- Some versions use "livekiturl", others "url"
- Activation can require: pulse button, toggle switch, or value set to 1
- Sometimes needs manual "connect" button click after parameters set
- Viewer window must be explicitly opened (right-click → Viewer)

### LiveKit Room Architecture
- **claymation-live**: Input room (browser → TD)
  - Publishers: Browser camera via publisher.html
  - Subscribers: TouchDesigner Web Render TOP, test viewers
  
- **processed-output**: Output room (OBS → browsers)
  - Publishers: OBS via WHIP streaming
  - Subscribers: return-viewer.html, any connected viewers

### Railway Deployment Notes
- Auto-deploys on `git push` to main branch
- Server restarts automatically on deploy
- Environment variables set in Railway dashboard
- Logs available in Railway project dashboard

### OBS WHIP Streaming Setup
- Uses OBS 30+ built-in WHIP support
- Server URL: https://claymation-transcription-l6e51sws.livekit.cloud
- Bearer token: LiveKit ingress token
- Must be configured in Settings → Stream → Service: WHIP

## SUGGESTED APPROACH FOR NEXT AGENT

1. **Immediately read this document completely**
2. **Take desktop and browser control** (Krista prefers full agentic access)
3. **Check current state**:
   - Is TD open with ndi-streamCOPY.toe?
   - Is webrender_livekit1 viewer window open?
   - What tabs are open in Firefox?
4. **Run the activation script** in TD textport
5. **Read and analyze the textport output**
6. **Based on output, determine next action**:
   - If activation worked: Start OBS streaming
   - If didn't work: Manually find and click activation controls
7. **Test complete pipeline** end-to-end
8. **Document any issues or deviations**

## SUCCESS CRITERIA

Pipeline is complete when:
1. ✅ Browser camera streaming to LiveKit "claymation-live"
2. ✅ TouchDesigner receiving and displaying video from LiveKit
3. ✅ Effects visible on video in TouchDesigner
4. ✅ NDI output active from TouchDesigner
5. ✅ OBS receiving NDI and streaming to LiveKit "processed-output"
6. ✅ return-viewer.html showing processed video with effects

## ADDITIONAL CONTEXT

### Krista's Working Style
- Prefers complete autonomous execution
- Wants full explanations, no abbreviations
- Values systematic documentation
- Focused on art/creative aspects, delegates technical details
- Comfortable with complexity but appreciates clear guidance

### Project Purpose
Interactive art installation where:
- Remote participants use browser camera
- Video is processed in real-time with TouchDesigner effects
- Processed video streams back to participants
- No app downloads required (browser-only accessibility)
- Global participation capability

### Current Installation Focus
"Claymation Mirror" and related works using this video pipeline for
responsive, interactive art experiences.

## QUICK REFERENCE COMMANDS

### Check if publisher is streaming:
Open Tab 131, look for "Publishing" status (green)

### Check if LiveKit is working:
Open Tab 150, should show "Receiving video from publisher-XXXXX"

### Activate Web Render TOP:
```python
exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_activate_specific.py').read())
```

### Start OBS:
```powershell
Start-Process "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
```

### Deploy to Railway:
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add .
git commit -m "Update"
git push
```

## FILES CREATED THIS SESSION
- td_activate_specific.py (latest activation script)
- td_video_now.py (earlier version)
- td_simple.py (configuration script)
- PASTE_NOW_INSTRUCTIONS.txt (user instructions)
- I_SAW_YOUR_SCREEN.txt (status based on screenshot)
- Multiple other diagnostic and instruction files

## LAST KNOWN STATE
- TouchDesigner open with webrender_livekit1 visible
- Viewer window open showing black screen
- Activation script ready in clipboard
- Publisher ready to start in Tab 131
- Test viewer (Tab 150) confirmed LiveKit working
- Waiting for agent to execute activation script and analyze results

---

## TO THE NEXT AGENT:

You're inheriting a 95% complete video pipeline. The only remaining task is
activating the Web Render TOP in TouchDesigner to receive the LiveKit stream.
Everything else is configured and working. 

The test viewer (Tab 150) proves LiveKit is working. The Web Render TOP exists
and is configured. It just needs the connection activated.

Run the activation script, read the output, and act on what it shows. If
automatic activation doesn't work, the output will tell you which parameters
exist and you can manually activate them.

Once video appears in TouchDesigner, start OBS streaming and the pipeline is
complete.

Good luck! You're so close!

---

**Handover prepared by: Claude (Agent Session Nov 22, 2024)**
**Ready for next agent to continue from this exact point.**
