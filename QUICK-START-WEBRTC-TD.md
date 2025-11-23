# 🚀 QUICK START: TouchDesigner WebRTC Bidirectional Streaming

## Current Status
- ✅ Server is running at `http://localhost:3000`
- ✅ LiveKit configured and ready
- ✅ New files created:
  - `td-bidirectional.html` - Full interactive bidirectional page
  - `td-auto-viewer.html` - Auto-connecting viewer (perfect for TouchDesigner)
  - `td_setup_helper.py` - Python script for TouchDesigner setup
  - `TOUCHDESIGNER-WEBRTC-INTEGRATION.md` - Complete integration guide

## Option 1: Simple Manual Setup (5 minutes)

### In TouchDesigner (ndi-streamCOPY.toe):

1. **Add Web Render TOP**
   - Press `Tab` → Type "web" → Select `Web Render TOP`
   - Name it: `webrender_input`

2. **Configure It**
   - Parameter `url`: `http://localhost:3000/td-auto-viewer.html`
   - Parameter `w`: `1920`
   - Parameter `h`: `1080`
   - Enable `Audio`: ✓ ON
   - Set `Active`: ✓ ON

3. **That's it for receiving!**
   - This TOP will auto-connect to LiveKit
   - When someone publishes, you'll see their video here
   - Connect this to your processing network

4. **For sending (you already have this!):**
   - Your current NDI Out setup works perfectly
   - Just make sure it's active and named properly
   - OBS will pick it up and publish via WHIP/LiveKit

### Testing:

1. **On your phone, open:**
   ```
   http://YOUR-COMPUTER-IP:3000/publisher.html
   ```
   (Get your IP with `ipconfig` in PowerShell)

2. **Click "Start Publishing"** on phone
   - Grant camera permissions
   - You should see yourself

3. **In TouchDesigner:**
   - The `webrender_input` TOP should now show your phone camera!
   - Process it through your network
   - Output via NDI

4. **On phone, open:**
   ```
   http://YOUR-COMPUTER-IP:3000/return-viewer.html
   ```
   - Click "Join Stream"
   - See your processed video!

## Option 2: Automated Python Setup (2 minutes)

### In TouchDesigner:

1. **Open Textport**
   - Alt + T

2. **Run the setup script:**
   ```python
   exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_helper.py').read())
   ```

3. **Follow the prompts**
   - It will create everything automatically!
   - Input → Processing → Output all set up

4. **Done!**
   - Three operators created and connected
   - Ready to use immediately

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  PHONE/BROWSER                                              │
│  http://localhost:3000/publisher.html                       │
│  📱 Camera + Microphone                                      │
└───────────────┬─────────────────────────────────────────────┘
                │ WebRTC
                ↓
┌─────────────────────────────────────────────────────────────┐
│  LIVEKIT CLOUD                                              │
│  Room: "claymation-live"                                    │
└───────────────┬─────────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────────┐
│  TOUCHDESIGNER                                              │
│                                                              │
│  [Web Render TOP: td-auto-viewer.html]                      │
│            ↓                                                 │
│  [Your Processing Network]                                  │
│  - Liquid Milk Balls effects                                │
│  - Color manipulation                                        │
│  - Whatever you want!                                        │
│            ↓                                                 │
│  [NDI Out TOP: "TD-LiveKit-Output"]                         │
└───────────────┬─────────────────────────────────────────────┘
                │ NDI
                ↓
┌─────────────────────────────────────────────────────────────┐
│  OBS STUDIO                                                  │
│  - NDI Source captures TD output                            │
│  - WHIP Plugin publishes to LiveKit                         │
└───────────────┬─────────────────────────────────────────────┘
                │ WebRTC (WHIP)
                ↓
┌─────────────────────────────────────────────────────────────┐
│  LIVEKIT CLOUD                                              │
│  Room: "processed-output"                                   │
└───────────────┬─────────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────────┐
│  PHONE/BROWSER                                              │
│  http://localhost:3000/return-viewer.html                   │
│  🎥 Sees processed video!                                    │
└─────────────────────────────────────────────────────────────┘
```

## Pages You Can Use

1. **td-bidirectional.html** - Interactive with controls
   - Shows both local and remote video
   - Manual START/STOP buttons
   - Status display
   - Good for testing/debugging

2. **td-auto-viewer.html** - Auto-connecting viewer
   - Just shows remote video fullscreen
   - Auto-connects on load
   - Auto-reconnects on disconnect
   - **RECOMMENDED for TouchDesigner Web Render TOP**

3. **publisher.html** - Remote users publish their camera
   - For phones/browsers that send camera to you
   - They open this URL

4. **return-viewer.html** - Remote users view processed output
   - For phones/browsers that receive your processed video
   - They open this URL after you process

## Network Access

### Same WiFi (Local Network):

1. Find your IP:
   ```powershell
   ipconfig
   ```
   Look for `IPv4 Address` (e.g., 192.168.1.100)

2. Share this URL with phones on same WiFi:
   ```
   http://192.168.1.100:3000/publisher.html
   ```

### Internet (Different Networks):

Use your Railway deployment:
```
https://marvelous-blessing-production-4059.up.railway.app/publisher.html
https://marvelous-blessing-production-4059.up.railway.app/return-viewer.html
```

## Troubleshooting

### Web Render TOP shows nothing
- Check URL is correct: `http://localhost:3000/td-auto-viewer.html`
- Make sure server is running
- Set Active OFF then ON to refresh

### "WAITING FOR STREAM" status
- Remote user hasn't started publishing yet
- Have them open publisher.html and click "Start Publishing"
- Check they're on the same network or using Railway URL

### No audio in TouchDesigner
- Make sure `Enable Audio` is checked on Web Render TOP
- Audio is embedded in the Web Render TOP
- Use Audio Device Out CHOP to output it

### Can't see processed video on phone
- Make sure OBS is streaming (WHIP configured)
- Check NDI Out is active in TouchDesigner
- Verify phone is connected to return-viewer.html

## Deploy to Internet

When ready to go live:

```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add .
git commit -m "Add TouchDesigner WebRTC integration"
git push
```

Railway auto-deploys in ~2 minutes!

## What You Have Now

✅ Receive remote camera/audio in TouchDesigner via WebRTC
✅ Process with your effects
✅ Send processed video back to remote viewers
✅ Works on local network or internet
✅ No apps needed - just browsers
✅ Low latency (sub-second with LiveKit)
✅ Scalable to multiple viewers

## Next Steps

1. Open TouchDesigner: `ndi-streamCOPY.toe`
2. Add Web Render TOP with auto-viewer page
3. Test with your phone
4. Connect to your processing network
5. Enjoy your interactive installation! 🎨✨

---

**Need help?** All the details are in:
- `TOUCHDESIGNER-WEBRTC-INTEGRATION.md` - Full guide
- `TOUCHDESIGNER-LIVEKIT-SETUP.md` - Original setup guide
- `td_setup_helper.py` - Automated setup script

**Ready to create magic!** 🚀
