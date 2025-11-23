# QUICK REFERENCE CARD - Video Processing Pipeline

## START EVERYTHING
```
Double-click: START_PIPELINE.bat
```

## ACCESS URLs
```
Camera Input:  http://localhost:3000/publisher.html
Video Output:  http://localhost:3000/return-viewer.html
```

## PIPELINE FLOW
```
Browser Camera 
  → LiveKit (claymation-live)
  → TouchDesigner (effects)
  → NDI Output
  → OBS
  → LiveKit (processed-output)
  → Browser Viewer
```

## QUICK CHECKS

### Is Server Running?
Check: http://localhost:3000
Should show: Server page

### Is OBS Streaming?
Check OBS window bottom-right
Should show: "Streaming" with green dot

### Is TouchDesigner Receiving?
Check: webrender_livekit_input operator
Should show: Camera feed

### Is NDI Working?
Check OBS: NDI Source
Should show: "TD-LiveKit-Output" with video

## TROUBLESHOOTING

### No Camera in TouchDesigner
- Check publisher.html clicked "Start Camera"
- Verify room name: "claymation-live"
- Check LiveKit credentials in .env

### No Video in Viewer
- Verify OBS is streaming (green "Streaming" indicator)
- Click "Join Stream" in return-viewer.html
- Refresh the viewer page

### OBS Won't Start Streaming
Tools → WebSocket Server Settings
  ☑ Enable WebSocket server
  Port: 4455
  Password: (empty)

### Server Won't Start
```bash
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
node server.js
```

## FILES YOU NEED

Essential:
- `START_PIPELINE.bat` - Main startup
- `README_FOR_KRISTA.md` - Full guide
- `COMPLETE_SOLUTION.md` - Technical docs

Optional:
- `start_obs_stream.py` - Just start OBS stream
- `start_pipeline.py` - Python version

## LIVEKIT DETAILS

Project: claymation-transcription-l6e51sws.livekit.cloud
API Key: APITw2Yp2Tv3yfg

Rooms:
- claymation-live (camera input)
- processed-output (viewer output)

## OBS SETTINGS

Service: WHIP
Server: https://claymation-transcription-l6e51sws.whip.livekit.cloud/w
Token: vZzz34cdzRkd

WebSocket:
Port: 4455
Password: (none)

NDI Source:
Name: TD-LiveKit-Output

## TOUCHDESIGNER OPERATORS

Input:
- webrender_livekit_input
- Room: claymation-live

Output:
- ndiout_livekit2
- Name: TD-LiveKit-Output

## STATUS INDICATORS

✓ Good:
- Server responds on port 3000
- TouchDesigner shows camera feed
- OBS shows "Streaming" status
- Viewer shows processed video

✗ Problem:
- Can't access localhost:3000
- TouchDesigner shows black screen
- OBS shows "Not Streaming"
- Viewer shows "Connecting..."

## QUICK TEST SEQUENCE

1. Run START_PIPELINE.bat
2. Wait for "All systems ready!"
3. Open publisher.html → Start Camera
4. Check TouchDesigner → See camera
5. Check OBS → See NDI video + "Streaming"
6. Open return-viewer.html → Join Stream
7. See yourself with effects!

## DEPLOYMENT (Future)

When ready for online access:
- Deploy server to Railway
- TouchDesigner + OBS stay local
- Share viewer URL with audience
- Unlimited simultaneous viewers

## SUPPORT NUMBERS

Server Port: 3000
WebSocket Port: 4455
LiveKit Rooms: 2 (input + output)
OBS Bitrate: 2500 kbps

---

Print this card and keep it nearby!
Last updated: November 22, 2025
