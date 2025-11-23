# YOUR DEPLOYMENT IS LIVE! 🎉

## Your Public URLs

**Railway Deployment**: https://liquid-milk-balls-web-production-2e8c.up.railway.app

### Access Your Pipeline:

**Camera Input** (for people sending their camera):
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html

**Video Viewer** (for people watching processed video):
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html

**Health Check** (verify server is running):
https://liquid-milk-balls-web-production-2e8c.up.railway.app/healthz

---

## Quick Tests (Do These Now!)

### Test 1: Server Health ✓
Open in your browser:
https://liquid-milk-balls-web-production-2e8c.up.railway.app/healthz

**Should show**: "ok"

If you see "ok", your server is running perfectly!

### Test 2: Camera Input Page ✓
Open in your browser:
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html

**You should see**:
- "Start Camera" button
- Clean interface
- LiveKit connection ready

### Test 3: Viewer Page ✓
Open in your browser:
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html

**You should see**:
- "Join Stream" button
- Ready to display video

---

## Complete End-to-End Pipeline Test

### Setup (On Your Computer)

1. **Start TouchDesigner** with your project file
2. **Run START_PIPELINE.bat** to start OBS streaming
3. Wait for "All systems ready!"

### Test From Your Phone

1. **On your phone**, open:
   https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html

2. Click **"Start Camera"**
3. Allow camera permissions
4. You should see yourself

### Verify in TouchDesigner (On Your Computer)

1. Look at your **webrender_livekit_input** operator in TouchDesigner
2. You should see the camera feed from your phone!
3. Your effects should be processing it

### View Processed Output

1. **On another device** (or different browser tab), open:
   https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html

2. Click **"Join Stream"**
3. You should see the processed video from TouchDesigner/OBS!

---

## The Complete Flow (Now Live!)

```
Phone Camera (anywhere in world)
  ↓
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
  ↓
Railway Server (generates LiveKit token)
  ↓
LiveKit Cloud (room: claymation-live)
  ↓
YOUR TouchDesigner (local computer - applies effects)
  ↓
YOUR OBS (local computer - streams via WHIP)
  ↓
LiveKit Cloud (room: processed-output)
  ↓
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html
  ↓
Viewer Sees Processed Video (anywhere in world)
```

---

## Share These Links

### For People to Send Their Camera:
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
```

### For People to Watch the Processed Video:
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html
```

### Create QR Codes (For Gallery)

You can generate QR codes for these URLs:
- Publisher QR code → People scan and start their camera
- Viewer QR code → People scan and watch the processed video

Use any free QR code generator like:
- qr-code-generator.com
- qrcode-monkey.com

---

## What's Deployed vs. What's Local

### Deployed on Railway (Globally Accessible):
✓ Web server (serves pages, generates tokens)
✓ Publisher page (camera input interface)
✓ Viewer page (video output interface)
✓ LiveKit integration (token generation)

### Still Running Locally (On Your Computer):
✓ TouchDesigner (video processing/effects)
✓ OBS (streaming to LiveKit)
✓ NDI (local video transport)

**Important**: Your computer must be running TouchDesigner + OBS for the pipeline to work!

---

## For Gallery Installations

### Setup:
1. Your laptop/computer at the venue running TouchDesigner + OBS
2. Large screen showing the viewer page
3. QR codes posted for visitors to scan
4. Visitors use their phones to send camera input
5. See themselves transformed on the big screen!

### Visitors Experience:
1. Scan QR code with phone
2. Click "Start Camera"
3. Allow camera permission
4. See themselves appear on big screen with effects
5. No app download needed!

---

## Monitoring Your Deployment

### Railway Dashboard:
- View logs in "Deployments" tab
- Monitor resource usage
- See request counts

### LiveKit Dashboard:
- https://cloud.livekit.io
- See active rooms
- Monitor participant count
- View bandwidth usage

---

## Troubleshooting

### "Can't access the page"
- Check your internet connection
- Verify the URL is exactly correct
- Try in incognito/private browser window

### "Camera won't start"
- Allow camera permissions in browser
- Try HTTPS (Railway automatically provides this)
- Check browser console for errors

### "No video in viewer"
- Make sure YOUR local TouchDesigner is running
- Make sure YOUR local OBS is streaming (run START_PIPELINE.bat)
- Check that someone is actually sending camera input

### "LiveKit connection failed"
- Verify Railway environment variables are set correctly
- Check Railway logs for errors
- Verify LiveKit credentials haven't expired

---

## Updating Your Deployment

Whenever you make changes to HTML pages or server code:

```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add [changed files]
git commit -m "Description of changes"
git push origin main
```

Railway automatically redeploys within 1-2 minutes!

---

## Custom Domain (Optional)

Want a nicer URL like `mirrors-echo.com`?

In Railway dashboard:
1. Settings → Domains
2. Click "Custom Domain"
3. Enter your domain
4. Follow DNS instructions
5. Railway provides free SSL certificate

---

## Cost & Usage

**Railway Free Tier**:
- $5 credit per month
- Your simple Node server: ~$1-2/month usage
- After free credit runs out, pay only for what you use

**LiveKit**:
- Check your LiveKit dashboard for usage
- Free tier includes generous usage
- Scale as needed

---

## Success Metrics

✓ **Server deployed** on Railway
✓ **Globally accessible** from any device
✓ **HTTPS enabled** automatically
✓ **Auto-redeploys** from GitHub
✓ **Environment variables** configured
✓ **Ready for production** use

---

## Next Steps

1. **Test the health endpoint** (should show "ok")
2. **Test publisher page** on your phone
3. **Start local pipeline** (TouchDesigner + OBS)
4. **Test complete flow** (camera → effects → viewer)
5. **Share with friends** to test remotely
6. **Create QR codes** for gallery installation

---

## You're Live!

Your "Mirror's Echo" installation is now globally accessible. Anyone with the URL can:
- Send their camera feed
- View the processed output
- Experience your art from anywhere

**Share these URLs and watch your installation come to life!** 🎨✨

---

**Your Deployment**: https://liquid-milk-balls-web-production-2e8c.up.railway.app
**Status**: Live and Ready
**Last Updated**: November 22, 2025
