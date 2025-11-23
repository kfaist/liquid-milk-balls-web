# TouchDesigner Bidirectional WebRTC/LiveKit Integration

## Overview

This guide shows you how to set up TouchDesigner to both SEND and RECEIVE audio and video through WebRTC/LiveKit, creating a complete bidirectional streaming setup.

## What This Does

```
┌──────────────────────────────────────────────────────────────┐
│  Remote User (Phone/Browser)                                 │
│  ↓ Sends camera/mic to LiveKit                               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  TouchDesigner                                                │
│  1. Web Render TOP → Displays remote feed                    │
│  2. Your processing network                                   │
│  3. Web Render TOP → Sends processed video back              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  Remote User (Phone/Browser)                                 │
│  ↑ Receives processed video/audio from LiveKit               │
└──────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. ✅ Server running at `http://localhost:3000` (already running!)
2. ✅ LiveKit credentials configured in `.env` (already done!)
3. ✅ TouchDesigner 2023.11600 or newer (you have it!)
4. ✅ New file: `td-bidirectional.html` (just created!)

## Step-by-Step Setup in TouchDesigner

### Part 1: Receive Remote Video/Audio (Input)

1. **Add Web Render TOP**
   - Press `Tab` → type "web" → select `Web Render TOP`
   - Name it: `webrender_input`

2. **Configure Web Render TOP**
   - URL: `http://localhost:3000/td-bidirectional.html`
   - Resolution: `1920 x 1080`
   - Enable Audio: ✓ ON
   - Active: ✓ ON

3. **The page will load - you'll see:**
   - Two video panels (Local Input | Remote Feed)
   - Status bar at bottom
   - START button

4. **Click START button in the Web Render TOP**
   - Use the mouse interaction in TouchDesigner
   - Status will change to "CONNECTED"
   - You should see "LOCAL INPUT" showing webcam
   - "REMOTE FEED" will show when someone connects

5. **Extract the video for processing**
   - The `webrender_input` TOP now contains the remote feed
   - Connect this to your processing network!

### Part 2: Send Processed Video Back (Output)

**Method A: Using Virtual Camera (Recommended for now)**

Your current setup with OBS Virtual Camera works! To complete the loop:

1. **In TouchDesigner:**
   - Your final processed output → `NDI Out TOP`
   - NDI Name: `TD-Processed`
   - Active: ✓ ON

2. **In OBS:**
   - Add NDI Source → Select `TD-Processed`
   - Start Virtual Camera
   - OR use WHIP plugin to publish directly to LiveKit

**Method B: Direct WebRTC from TouchDesigner (Advanced)**

This requires a separate Web Render TOP that captures TouchDesigner's output:

1. **Create a canvas/window with your output**
   - Use a `Container COMP` with your processed video
   - Or use a second `Web Render TOP` with a publisher page

2. **Use the publisher page:**
   - Create another `Web Render TOP`
   - URL: `http://localhost:3000/publisher.html`
   - This page can access OBS Virtual Camera
   - Click "Start Publishing" to send to LiveKit

### Part 3: Testing the Complete Loop

1. **On your phone or another browser, open:**
   ```
   http://YOUR-IP:3000/publisher.html
   ```
   (Replace YOUR-IP with your computer's local IP, like 192.168.1.x)

2. **Click "Start Publishing" on phone**
   - Grant camera/microphone permissions
   - You should see yourself on the phone

3. **In TouchDesigner Web Render TOP**
   - The "REMOTE FEED" panel should now show your phone's camera!
   - Status should say "RECEIVING VIDEO FROM..."

4. **Process the video in TouchDesigner**
   - Connect `webrender_input` to your effects network
   - Apply your liquid milk balls effects!

5. **Send processed video back**
   - Output → NDI → OBS → LiveKit
   - OR set up second Web Render TOP with publisher

6. **On phone, open:**
   ```
   http://YOUR-IP:3000/return-viewer.html
   ```
   - Click "Join Stream"
   - You should see your processed video!

## Current File Structure

Your TouchDesigner file: `ndi-streamCOPY.toe`

It should now have:
- `webrender_input` - Receives remote camera via LiveKit
- Your existing processing network
- `ndi_out` - Sends to OBS for publishing

## Audio Handling

The `td-bidirectional.html` page handles audio automatically:
- Remote audio is available in the Web Render TOP
- Use `Audio Device Out CHOP` to output audio from TouchDesigner
- Audio routing: Web Render → CHOP → Audio Device Out

## Troubleshooting

### "DISCONNECTED" status won't change
- Check server is running: `http://localhost:3000`
- Verify `.env` has LiveKit credentials
- Check browser console in Web Render TOP for errors

### No remote video showing
- Ensure remote user clicked "Start Publishing"
- Check they granted camera permissions
- Verify both are in the same room (`claymation-live`)

### Can't click START button
- Enable mouse interaction on Web Render TOP
- Or use TouchDesigner's Panel COMP for better control

### Video is black
- Check Web Render TOP is Active
- Verify URL is correct
- Try refreshing: set Active OFF then ON

## Network Configuration for Remote Access

To allow phone/remote users to connect:

1. **Find your local IP:**
   ```powershell
   ipconfig
   ```
   Look for IPv4 Address (e.g., 192.168.1.100)

2. **Test from phone on same WiFi:**
   ```
   http://192.168.1.100:3000/publisher.html
   ```

3. **For internet access (not on same WiFi):**
   - Use your Railway deployment:
   ```
   https://marvelous-blessing-production-4059.up.railway.app/publisher.html
   ```

## Next Steps

1. ✅ Test receiving remote video in TouchDesigner
2. ✅ Connect to your processing network
3. ✅ Set up output path (NDI → OBS → LiveKit)
4. ✅ Test complete loop with phone
5. 🚀 Deploy to Railway for internet access!

## Quick Command Reference

**Start server:**
```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
npm start
```

**Deploy to Railway:**
```powershell
git add .
git commit -m "Add TouchDesigner bidirectional streaming"
git push
```

**Test pages:**
- Bidirectional: http://localhost:3000/td-bidirectional.html
- Publisher (remote): http://localhost:3000/publisher.html
- Return viewer: http://localhost:3000/return-viewer.html

---

Ready to create amazing interactive installations! 🎨✨
