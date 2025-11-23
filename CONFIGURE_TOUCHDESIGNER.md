# CONFIGURE TOUCHDESIGNER WEBRENDER - STEP BY STEP

## Your Fresh LiveKit Token (Valid for 24 hours)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJzdWIiOiJ0b3VjaGRlc2lnbmVyLXJlY2VpdmVyIiwiaWF0IjoxNzYzODAxODQ5LCJuYmYiOjE3NjM4MDE4NDksImV4cCI6MTc2Mzg4ODI0OX0.7r4VZzzAnbh-On6cw1D2r2kCN84K4QCcorE5-1ZyoA0
```

---

## Step 1: Find Your WebRender Operator in TouchDesigner

1. **Open TouchDesigner** (already open)
2. Press **Alt+L** (opens search dialog)
3. Type: **webrender**
4. Look for an operator named something like:
   - webrender_livekit_input
   - webRenderTOP1
   - webrender1

**If you FIND it**: Go to Step 2
**If you DON'T find it**: Go to "Create New WebRender Operator" section below

---

## Step 2: Configure the WebRender Operator

1. **Click on the webrender operator** to select it
2. **Right-click** and choose **Parameters**
3. In the parameters panel, set these EXACT values:

### Required Parameters:

**Room Name:**
```
claymation-live
```

**Server URL:**
```
wss://claymation-transcription-l6e51sws.livekit.cloud
```

**Token** (copy the ENTIRE token from above):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJzdWIiOiJ0b3VjaGRlc2lnbmVyLXJlY2VpdmVyIiwiaWF0IjoxNzYzODAxODQ5LCJuYmYiOjE3NjM4MDE4NDksImV4cCI6MTc2Mzg4ODI0OX0.7r4VZzzAnbh-On6cw1D2r2kCN84K4QCcorE5-1ZyoA0
```

**Active:** Make sure this is **ON** (checked)

4. **Click anywhere** outside the parameters panel to apply

---

## Step 3: Test the Connection

1. **On your phone**, open:
   https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html

2. Click **"Start Camera"**
3. Allow camera permissions
4. **You should see yourself** in the publisher page

5. **Back in TouchDesigner**:
   - Look at your webrender operator
   - You should see your phone's camera feed!
   - It might take 3-5 seconds to connect

---

## If You DON'T Have a WebRender Operator Yet

### Create New WebRender Operator:

1. In TouchDesigner, press **Tab** key
2. In the operator menu, type: **webrender**
3. Select **webRenderTOP**
4. Click to place it in your network

5. **Now configure it** using Step 2 above (set Room Name, Server URL, Token)

---

## Troubleshooting

### Black Screen in WebRender?

**Check 1**: Is publisher sending camera?
- Go to publisher.html on your phone
- Make sure you see your camera
- Try refreshing the page

**Check 2**: Are the parameters correct?
- Room Name MUST be exactly: claymation-live
- Server URL MUST be exactly: wss://claymation-transcription-l6e51sws.livekit.cloud
- Token MUST be the complete token (no spaces, no line breaks)

**Check 3**: Is Active turned on?
- Make sure the Active parameter is checked

**Check 4**: Wait a few seconds
- Connection can take 3-5 seconds
- LiveKit needs to establish WebRTC connection

### Error Messages?

**Look at the operator info panel** (bottom of TouchDesigner)

Common errors:
- "Invalid token" → Token expired or incorrect
- "Room not found" → Room name is wrong
- "Connection failed" → Server URL is wrong

---

## After It's Working

Once you see your phone's camera in the webrender operator:

1. **Connect it to your effect chain**
   - Wire the webrender output to your effects
   
2. **Check the NDI output**
   - Make sure ndiout_livekit2 is outputting "TD-LiveKit-Output"
   
3. **Verify OBS is receiving**
   - OBS should show the NDI source with video

4. **Test the viewer**
   - Open return-viewer.html
   - Click "Join Stream"
   - See the processed video!

---

## Quick Reference

**If token expires** (after 24 hours):
- Run: `python generate_td_token.py`
- Copy the new token
- Paste into webrender parameters

**Room Configuration:**
- Input room (where camera goes): claymation-live
- Output room (where processed video goes): processed-output
- WebRender connects to: claymation-live (input)

---

## Next Steps

Once webrender is showing your phone's camera:

1. [ ] Verify effects are being applied
2. [ ] Check NDI output is working
3. [ ] Confirm OBS is streaming
4. [ ] Test viewer page shows processed video

**Tell me what you see in the webrender operator and I'll help with the next steps!**
