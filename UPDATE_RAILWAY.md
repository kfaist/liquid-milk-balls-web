# UPDATE RAILWAY - Quick Guide

## Your Setup
- ✓ GitHub repo: https://github.com/kfaist/liquid-milk-balls-web
- ✓ Railway project already exists
- ✓ Code just pushed to GitHub

---

## Step 1: Railway Will Auto-Deploy

Since you already have Railway connected to GitHub:
- Railway automatically detected your push
- It's probably deploying right now
- Check your Railway dashboard to see the build

---

## Step 2: Add/Verify Environment Variables

Go to your Railway dashboard and add these variables if not already set:

### In Railway Dashboard:
1. Click on your project
2. Click "Variables" tab
3. Add or verify these 5 variables:

```
LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

**Copy/Paste Method** (Faster):
- Click "RAW Editor" button in Variables tab
- Paste all 5 lines at once
- Click "Update Variables"

---

## Step 3: Get Your Railway URL

In Railway dashboard:
1. Look for "Deployments" or "Settings" tab
2. Find your public URL (something like: `https://liquid-milk-balls-web-production.up.railway.app`)

**Or Generate a New Domain**:
- Settings → Domains → "Generate Domain"
- Railway creates a nice URL for you

---

## Step 4: Test Your Deployment

### Quick Test:
Visit: `https://your-railway-url/healthz`

Should show: **ok**

### Full URLs:
- **Camera Input**: `https://your-railway-url/publisher.html`
- **Video Viewer**: `https://your-railway-url/return-viewer.html`

---

## Step 5: Test the Complete Pipeline

### On Your Computer (Local):
1. Make sure TouchDesigner is running
2. Run `START_PIPELINE.bat` (to start OBS streaming)

### From Any Device (Remote):
1. Visit your Railway URL + `/publisher.html`
2. Click "Start Camera"
3. Allow camera
4. Visit your Railway URL + `/return-viewer.html` on another device
5. Click "Join Stream"
6. Should see processed video from TouchDesigner!

---

## What Railway Does

**Railway hosts**:
- Web server (server.js)
- HTML pages (publisher.html, return-viewer.html)
- Token generation for LiveKit

**Still local (your computer)**:
- TouchDesigner (processing video)
- OBS (streaming to LiveKit)

---

## Next Time You Update

Just push to GitHub:
```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add [files]
git commit -m "description"
git push origin main
```

Railway automatically redeploys!

---

## Your Railway URL

Once you get your Railway URL, you can share:
- `https://your-url/publisher.html` (for people to send their camera)
- `https://your-url/return-viewer.html` (for people to watch processed video)

Perfect for gallery installations!

---

**Need your Railway URL?** 
Check your Railway dashboard → Deployments or Settings → Domains
