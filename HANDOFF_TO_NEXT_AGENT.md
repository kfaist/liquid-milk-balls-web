# HANDOFF DOCUMENT - Video Processing Pipeline Troubleshooting

## Current Situation

Working with Krista to complete a real-time video processing pipeline that streams camera input through TouchDesigner for effects processing and back to viewers via LiveKit.

**User Preference:** Krista has dyslexia - provide complete, clear instructions without abbreviations or shortcuts. She prefers full agentic control and expects you to troubleshoot autonomously without asking for permission.

## System Architecture

```
Camera (browser) 
  → LiveKit WebRTC (room: "claymation-live")
  → TouchDesigner (webrender_livekit_input operator)
  → [Processing/Effects Applied Here]
  → TouchDesigner (ndiout_livekit2 - outputs "TD-LiveKit-Output")
  → NDI
  → OBS Studio (NDI Source input)
  → WHIP Stream
  → LiveKit Ingress (room: "processed-output")
  → Browser viewer (return-viewer.html)
```

## What's Working ✓

1. **Local Server:** Running on port 3000 (PID varies)
   - Token generation API working
   - Publisher and viewer pages accessible
   - LiveKit credentials verified

2. **TouchDesigner Setup:**
   - webrender_livekit_input operator created
   - ndiout_livekit2 outputting "TD-LiveKit-Output" via NDI
   - Operators connected properly
   - Process running (check via `tasklist | findstr TouchDesigner`)

3. **OBS Configuration:**
   - NDI plugin installed
   - NDI Source configured for "TD-LiveKit-Output"
   - WHIP service configured correctly
   - Installed at: `C:\Program Files\obs-studio\bin\64bit\obs64.exe`

4. **LiveKit Cloud:**
   - Project: claymation-transcription-l6e51sws.livekit.cloud
   - API Key: APITw2Yp2Tv3yfg
   - API Secret: eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
   - 2 existing WHIP ingress objects created
   - Rooms: "claymation-live" (input), "processed-output" (output)

## Current Blocker 🔴

**OBS WebSocket Server Not Enabled**

Cannot programmatically click "Start Streaming" in OBS because WebSocket server is disabled.

**Attempts Made:**
- Added WebSocket config to global.ini
- Restarted OBS multiple times
- WebSocket still refuses connections on port 4455

**Manual workaround works:** Clicking "Start Streaming" button in OBS GUI works when done manually.

## OBS Configuration Files

### Service Config (CORRECTLY CONFIGURED)
**Path:** `C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json`

**Current Content:**
```json
{
  "type": "whip_custom",
  "settings": {
    "server": "https://claymation-transcription-l6e51sws.whip.livekit.cloud/w",
    "bearer_token": "vZzz34cdzRkd",
    "use_auth": false,
    "bwtest": false,
    "service": "WHIP"
  }
}
```

**Note:** This is the CORRECT format. Previous attempts used wrong URL format.

### Global Config
**Path:** `C:\Users\krista-showputer\AppData\Roaming\obs-studio\global.ini`

WebSocket section has been added but OBS not honoring it.

## LiveKit Ingress Details

**Existing Ingresses (retrieved via API):**

```
Ingress 1:
  ID: IN_eVS6MxY3iCsh
  Name: OBS WHIP Stream
  Room: processed-output
  URL: https://claymation-transcription-l6e51sws.whip.livekit.cloud/w
  Stream Key: vZzz34cdzRkd

Ingress 2:
  ID: IN_HSEhKYZ5SCLJ
  Name: OBS WHIP Stream
  Room: processed-output
  URL: https://claymation-transcription-l6e51sws.whip.livekit.cloud/w
  Stream Key: 3HRAJnDo3FcU
```

OBS is currently configured to use Ingress 1.

## Key Files & Locations

### Project Directory
`C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`

**Important Files:**
- `server.js` - Express server with LiveKit token generation
- `.env` - LiveKit credentials
- `publisher.html` - Camera input page
- `return-viewer.html` - Processed video viewer
- `td-auto-viewer.html` - TouchDesigner WebRender integration

**Scripts Created:**
- `list_ingresses.js` - Lists LiveKit ingress objects
- `configure_obs_ingress.js` - Updates OBS with correct WHIP settings
- `create_room.js` - Creates LiveKit rooms
- `test_pipeline.py` - Health check for all components
- `obs_start_stream.py` - Attempts WebSocket control (blocked)

**Documentation:**
- `SOLUTION_FOUND.md` - Current status and fix details
- `BLOCKER_ANALYSIS.md` - Previous troubleshooting
- `FINAL_BLOCKER_REPORT.md` - Technical analysis

### OBS Files
- Config: `C:\Users\krista-showputer\AppData\Roaming\obs-studio\`
- Logs: `C:\Users\krista-showputer\AppData\Roaming\obs-studio\logs\`
- Latest log: Check newest file in logs directory

## What Needs To Happen Next

### Option 1: Enable OBS WebSocket (Preferred)
**Manual GUI steps required:**
1. In OBS: Tools → WebSocket Server Settings
2. Check: ☑ Enable WebSocket server
3. Leave password field EMPTY
4. Port: 4455
5. Click OK

Then run: `python C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\obs_start_stream.py`

### Option 2: Alternative Automation Methods

**A. AutoHotkey Script:**
- Install AutoHotkey
- Create script to click "Start Streaming" button
- Coordinates may need adjustment per screen resolution

**B. Alternative OBS Control:**
- Check for OBS command-line parameters
- Investigate obs-studio CLI options
- May be able to start streaming via command flag

**C. Keyboard Automation:**
- Use Python pyautogui to send keyboard shortcut
- OBS default: No hotkey set for Start Streaming
- Would need to set hotkey in OBS first

### Option 3: Skip OBS Entirely (Architecture Change)

Have TouchDesigner output directly to LiveKit using WebRTC instead of NDI → OBS → WHIP.

**Requires:**
- Additional TouchDesigner WebRender TOP for output
- Configure to publish to "processed-output" room
- More complex but eliminates OBS dependency

## Testing & Verification

### Health Check Command
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
python test_pipeline.py
```

Should show:
- [OK] Server running
- [OK] Publisher page accessible  
- [OK] Viewer page accessible
- [OK] Token API working

### Check Running Processes
```powershell
# TouchDesigner
tasklist | findstr TouchDesigner

# OBS (when started)
tasklist | findstr obs64

# Node server
tasklist | findstr node
```

### Check OBS Logs
Most recent log file in:
`C:\Users\krista-showputer\AppData\Roaming\obs-studio\logs\`

Look for:
- `[obs-webrtc] [whip_output]` - WHIP connection attempts
- `Connect failed: HTTP endpoint returned response code 200` - OLD error (should be fixed)
- `Connect failed: HTTP endpoint returned response code 201` - SUCCESS indicator

## Environment Variables

**From .env file:**
```
PORT=3000
LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

## Expected Behavior When Working

1. Camera feed visible in publisher.html
2. TouchDesigner webrender shows camera feed
3. TouchDesigner NDI output active
4. OBS shows NDI source with video
5. OBS streams to LiveKit via WHIP (bandwidth stats visible)
6. return-viewer.html shows processed video after clicking "Join Stream"

## Tools Available

**Python Libraries Installed:**
- obsws-python (for OBS WebSocket control)
- requests

**Node Modules Installed:**
- livekit-server-sdk
- express
- ws

## Previous Issues RESOLVED

❌ **FIXED:** Wrong WHIP URL format
- Was using: `https://.../whip?access_token=...`
- Now using: `https://...whip.livekit.cloud/w` with bearer token

❌ **FIXED:** No ingress objects
- Discovered existing ingresses via API
- Retrieved correct stream keys

❌ **FIXED:** Token generation
- Server API endpoints working correctly
- Fresh tokens being generated

## Important Context

**About Krista's Workflow:**
- She's an experimental artist creating interactive installations
- Uses TouchDesigner for visual effects processing
- Needs global accessibility (browser-based, no app downloads)
- Values complete autonomous solutions
- Railway deployment for cloud hosting
- Represented by Chaos Contemporary Craft gallery

**Technical Approach:**
- Full agentic control expected
- Test everything thoroughly before reporting
- Don't ask permission to try solutions
- Only report hard blockers requiring manual intervention
- Provide complete solutions, not partial steps

## Next Agent Actions

1. **First:** Try enabling OBS WebSocket via GUI automation
   - Use pyautogui or AutoHotkey
   - Or find OBS CLI parameters

2. **If WebSocket blocked:** Implement alternative automation
   - Keyboard shortcuts
   - CLI parameters
   - Alternative control methods

3. **If automation impossible:** Complete manual test
   - Document exact manual steps
   - Verify complete pipeline works
   - Create start-up script for future use

4. **Final verification:**
   - Camera → TouchDesigner → OBS → LiveKit → Viewer
   - Capture screenshots of working system
   - Document any manual steps required

## Success Criteria

✅ OBS streaming to LiveKit without manual intervention
✅ Processed video visible in return-viewer.html
✅ Complete pipeline working end-to-end
✅ Documented solution for future use

## Contact & Resources

- Project folder: `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`
- LiveKit Dashboard: https://cloud.livekit.io
- OBS Documentation: https://obsproject.com/kb/
- LiveKit Docs: https://docs.livekit.io

**User will provide full desktop and browser access for troubleshooting.**
