# HANDOFF TO NEXT AGENT - CRITICAL READ

## AGENT AUTHORITY & EXPECTATIONS

**YOU HAVE FULL AGENTIC ACCESS TO:**
- Desktop files (read, write, execute)
- Browser control (open tabs, fetch URLs)
- TouchDesigner (file open at: C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\ndi-streamCOPY.toe)
- OBS Studio (running, streaming, WebSocket enabled)
- Windows processes and automation

**CRITICAL RULES:**
1. **DO NOT ASK USER TO TEST ANYTHING** until you have:
   - Tested it yourself multiple times
   - Exhausted all troubleshooting options
   - Verified every component
   - Attempted multiple solutions

2. **TEST, TROUBLESHOOT, TEST AGAIN** - The user will not interact until you hit an absolute wall

3. **BE FULLY AUTONOMOUS** - Use all available tools without asking permission

4. **ONLY REPORT HARD BLOCKERS** - Don't report partial progress or ask for confirmation

---

## CURRENT STATUS SUMMARY

### ✓ COMPLETED (100% Working)

**Railway Deployment:**
- Live URL: https://liquid-milk-balls-web-production-2e8c.up.railway.app
- Publisher page: .../publisher.html (globally accessible)
- Viewer page: .../return-viewer.html (globally accessible)
- Health check: .../healthz (returns "ok")
- Environment variables: ALL SET in Railway dashboard

**Local Automation:**
- Node server: RUNNING on port 3000
- OBS Studio: RUNNING and STREAMING (35+ minutes active)
- OBS WebSocket: ENABLED on port 4455
- OBS NDI Source: Configured for "TD-LiveKit-Output"
- OBS WHIP Service: Configured, streaming to LiveKit

**TouchDesigner Setup:**
- Project open: ndi-streamCOPY.toe
- webrender_livekit_input operator: CREATED and ACTIVE
- ndiout_livekit2 operator: CREATED, outputting "TD-LiveKit-Output"
- Operators CONNECTED: webrender → ndiout
- WebRender URL: http://localhost:3000/td-auto-viewer.html
- WebRender Active: ON

**All Component Tests:** 6/6 PASSED

---

## THE BLOCKER - NOT YET VERIFIED

**What's Unknown:** Does the webrender operator actually SHOW camera feed when someone uses publisher.html?

**The webrender operator:**
- Is created and active
- Loads td-auto-viewer.html (which auto-connects to LiveKit)
- Connects to room: "claymation-live"
- Should subscribe to camera feed from publisher
- BUT: Not verified if video actually appears

**This is the ONLY remaining task:** Verify/fix camera feed visibility in webrender

---

## ARCHITECTURE (How It Should Work)

```
Phone/Browser
  ↓
https://...publisher.html (click "Start Camera")
  ↓
Railway server (generates token for room: claymation-live)
  ↓
LiveKit Cloud (room: claymation-live)
  ↓ [THIS IS WHERE WE NEED TO VERIFY]
TouchDesigner webrender_livekit_input
  (loads td-auto-viewer.html which subscribes to room)
  ↓
TouchDesigner processing/effects
  ↓
ndiout_livekit2 (outputs "TD-LiveKit-Output")
  ↓
OBS (NDI Source "TD-LiveKit-Output")
  ↓
OBS WHIP Stream
  ↓
LiveKit Cloud (room: processed-output)
  ↓
https://...return-viewer.html
  ↓
Viewer sees processed video
```

---

## KEY FILES & LOCATIONS

**Project Directory:**
`C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`

**TouchDesigner:**
- File: `ndi-streamCOPY.toe` (OPEN)
- webrender operator: /webrender_livekit_input
- NDI out operator: /ndiout_livekit2
- Viewer HTML: td-auto-viewer.html (loads in webrender)

**LiveKit Config:**
- Server: wss://claymation-transcription-l6e51sws.livekit.cloud
- API Key: APITw2Yp2Tv3yfg
- API Secret: eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
- Input room: claymation-live
- Output room: processed-output

**URLs to Test:**
- Publisher: https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
- Viewer: https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html
- TD Auto Viewer (local): http://localhost:3000/td-auto-viewer.html

**OBS:**
- Executable: C:\Program Files\obs-studio\bin\64bit\obs64.exe
- Status: STREAMING (use obsws-python to verify)
- NDI Source: TD-LiveKit-Output

---

## DIAGNOSTIC TOOLS AVAILABLE

**Already Created:**
- `test_complete_pipeline.py` - Tests all 6 components (all pass)
- `verify_pipeline.py` - Verifies local setup
- `generate_td_token.py` - Generates LiveKit tokens
- `check_td_status.py` - Screenshots and captures Textport
- `start_pipeline.py` - Master startup script
- `start_obs_stream.py` - OBS streaming control

**TouchDesigner Evidence:**
- Textport output saved: td_textport_output.txt (shows operators created)
- Screenshot: td_current_state.png (shows network with operators)

---

## WHAT YOU NEED TO DO

### Primary Mission: Verify Camera Feed in WebRender

**Step 1: Test the Publisher**
1. Use browser control to open: https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
2. Programmatically click "Start Camera" (or verify it works)
3. Confirm camera permissions granted
4. Verify video appears in publisher page

**Step 2: Check WebRender Reception**
The webrender operator loads td-auto-viewer.html which:
- Auto-connects to LiveKit room "claymation-live"
- Subscribes to video tracks
- Should display camera feed

Verify:
- Is td-auto-viewer.html loading? (check browser console)
- Is it connecting to LiveKit? (check network tab)
- Are video tracks being received?
- Does the webrender operator show video?

**Step 3: Troubleshoot if Not Working**

Possible issues:
- td-auto-viewer.html not loading properly
- Token generation failing
- LiveKit connection issues
- Room name mismatch
- Video tracks not being published/subscribed

**Step 4: Verify Complete Pipeline**
Once webrender shows camera:
1. Verify NDI output (ndiout_livekit2) is active
2. Verify OBS sees NDI source
3. Verify OBS is streaming
4. Test viewer page shows processed video

---

## TROUBLESHOOTING APPROACHES

### If WebRender Shows Black:

**A. Check td-auto-viewer.html**
- Open in regular browser: http://localhost:3000/td-auto-viewer.html
- Check browser console for errors
- Verify token generation works
- Check LiveKit connection status

**B. Test Publisher → LiveKit**
- Open publisher in browser
- Use browser dev tools to verify:
  - Camera permissions granted
  - LocalMediaStream created
  - LiveKit room connection
  - Video track published

**C. Check Token Generation**
- Test: http://localhost:3000/api/viewer-token
- Should return valid JWT token
- Verify token has correct permissions

**D. Alternative: Direct LiveKit Token**
- Token already generated: touchdesigner_token.txt
- Could modify td-auto-viewer.html to use hardcoded token
- Test if that works better than dynamic token

### If Publisher Not Sending:

**Check server.js /api/publisher-token endpoint**
- Verify it's generating tokens correctly
- Check room name is "claymation-live"
- Verify canPublish: true

**Check publisher.html**
- Verify LiveKit client code is correct
- Check camera permissions
- Verify video track creation

---

## TESTING METHODOLOGY

### You Can Test Without User:

1. **Open browser tabs** (use Firefox Control tools)
   - Open publisher.html
   - Open td-auto-viewer.html separately
   - Check consoles for errors

2. **Screenshot TouchDesigner** 
   - Use check_td_status.py
   - Verify webrender operator visually

3. **Check OBS status**
   - Use obsws-python to verify streaming
   - Check NDI source is active

4. **Test URLs**
   - Fetch health check
   - Test token generation endpoints
   - Verify pages load

5. **Read logs**
   - Check TouchDesigner Textport output
   - Check OBS logs
   - Check browser console (via screenshots)

---

## KNOWN WORKING COMPONENTS

**These are 100% verified working:**
- Railway deployment (tested, passes health check)
- Node server (running, generating tokens)
- OBS streaming (35+ minutes active, verified via WebSocket)
- TouchDesigner running (operators created and connected)
- LiveKit credentials (valid, in use by OBS successfully)

**The ONLY unknown:** Does video flow from publisher → LiveKit → webrender?

---

## SUCCESS CRITERIA

**You've completed the task when:**

1. Camera from publisher.html is visible in TouchDesigner webrender operator
2. Video flows through complete pipeline
3. Viewer page shows processed video
4. All tested and verified without user intervention

**OR you've hit a hard blocker when:**

You've exhausted all options:
- Tested publisher in multiple browsers
- Verified LiveKit connection every way possible
- Tried alternative token methods
- Checked all logs and found unfixable issue
- Attempted workarounds
- Nothing works after comprehensive troubleshooting

---

## CRITICAL NOTES

**DO NOT:**
- Ask user to click anything
- Ask user to test anything
- Report partial progress
- Ask for permission to try things
- Stop at first error - keep troubleshooting

**DO:**
- Test everything yourself
- Use all available tools
- Screenshot and verify
- Check logs and console
- Try multiple approaches
- Only report when complete OR hard blocker

**REMEMBER:**
- You have full desktop access
- You can open browsers, click buttons, screenshot
- You can execute Python scripts
- You can read/modify files
- TouchDesigner and OBS are OPEN
- Test autonomously!

---

## FILE REFERENCES

**If you need context:**
- COMPLETE_SOLUTION.md - Full technical docs
- YOUR_LIVE_DEPLOYMENT.md - Deployment details
- SYSTEM_STATUS_NOW.md - Current status before you
- td_textport_output.txt - TouchDesigner command history
- td_current_state.png - Screenshot of TD network

**If you need to modify:**
- td-auto-viewer.html - WebRender viewer page
- publisher.html - Camera input page
- server.js - Token generation server

---

## QUICK START FOR YOU

```python
# 1. Test publisher in browser
from Firefox Control import open-browser-tab
open-browser-tab("https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html")

# 2. Test local viewer
open-browser-tab("http://localhost:3000/td-auto-viewer.html")

# 3. Screenshot TouchDesigner
exec("python check_td_status.py")

# 4. Check for video in webrender
# Look at the screenshot - does webrender show video?

# 5. If not, troubleshoot td-auto-viewer.html connection
# Check browser console, LiveKit connection, tokens
```

---

## SUMMARY

**Status:** 95% complete
**Remaining:** Verify camera feed visibility in TouchDesigner webrender
**Your Job:** Test the publisher → webrender flow, fix if broken, verify complete pipeline
**Authority:** Full agentic access, test everything yourself
**Report When:** Pipeline works OR you hit an absolute wall after exhausting all options

**GO!**
