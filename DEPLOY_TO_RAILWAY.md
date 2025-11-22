# RAILWAY DEPLOYMENT GUIDE

## Quick Deploy (5 Minutes)

### Step 1: Commit Your Code (1 min)

Open PowerShell in your project folder and run:

```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web

# Add only the essential files for deployment
git add server.js package.json package-lock.json railway.json
git add publisher.html return-viewer.html index.html
git add .gitignore
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Create Railway Project (2 min)

1. Go to https://railway.app
2. Click "Start a New Project"
3. Click "Deploy from GitHub repo"
4. Select your repository: **kfaist/liquid-milk-balls-web**
5. Railway will automatically detect it's a Node.js project

### Step 3: Add Environment Variables (2 min)

In Railway dashboard, click on your project, then "Variables" tab and add:

```
LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

**Optional** (if you plan to add payment features later):
```
STRIPE_SECRET_KEY=(your stripe key if needed)
STRIPE_PUBLISHABLE_KEY=(your stripe key if needed)
```

### Step 4: Deploy!

Railway will automatically deploy. Wait about 2 minutes.

### Step 5: Get Your URL

Once deployed, Railway gives you a URL like:
`https://your-app.up.railway.app`

Your pages will be:
- Camera Input: `https://your-app.up.railway.app/publisher.html`
- Video Output: `https://your-app.up.railway.app/return-viewer.html`

---

## How It Works

### What Gets Deployed
- **Web server** (server.js) - Runs in Railway's cloud
- **HTML pages** - Served from Railway
- **LiveKit integration** - Connects to your existing LiveKit project

### What Stays Local
- **TouchDesigner** - Still runs on your computer
- **OBS** - Still runs on your computer
- **NDI** - Still runs locally

### The Complete Flow (After Deployment)

```
Remote User's Camera (anywhere in world)
  ↓
Railway Server (generates token)
  ↓
LiveKit Cloud (room: claymation-live)
  ↓
YOUR TouchDesigner (running locally)
  ↓
YOUR OBS (running locally, streaming via WHIP)
  ↓
LiveKit Cloud (room: processed-output)
  ↓
Remote User's Browser (viewing processed video)
```

---

## Testing Your Deployment

### Test 1: Server Health
Visit: `https://your-app.up.railway.app/healthz`
Should show: "ok"

### Test 2: Camera Input
1. Visit: `https://your-app.up.railway.app/publisher.html`
2. Click "Start Camera"
3. Allow camera permission
4. Your camera should appear

### Test 3: Complete Pipeline
1. Make sure YOUR local TouchDesigner is running
2. Make sure YOUR local OBS is streaming (run START_PIPELINE.bat)
3. Remote person visits publisher.html (starts camera)
4. Remote person visits return-viewer.html (sees processed video)

---

## Important Notes

### You Still Need Local Components
- TouchDesigner must be running on your computer
- OBS must be streaming from your computer
- The web server in Railway just handles:
  - Serving HTML pages
  - Generating LiveKit tokens
  - No video processing happens in Railway

### For Gallery Installation
Perfect setup:
- Your computer at the venue running TouchDesigner + OBS
- Visitors use their phones to access Railway URLs
- No downloads needed
- No local network setup

### Cost
Railway free tier includes:
- $5 of usage per month
- Your simple Node server will likely use ~$1-2/month
- After free credit, you pay only for what you use

---

## Troubleshooting

### "Application failed to respond"
Check Railway logs:
1. In Railway dashboard, click your project
2. Click "Deployments"
3. Click latest deployment
4. View logs

Common issues:
- Missing environment variables
- Port binding (Railway handles this automatically)

### "Can't connect to LiveKit"
- Verify all 5 environment variables are set in Railway
- Check they match your .env file exactly
- No typos in the URLs or keys

### "Video not showing in viewer"
- Make sure YOUR local OBS is streaming
- Check YOUR local TouchDesigner is running
- Verify START_PIPELINE.bat succeeded locally

---

## Updating Your Deployment

Whenever you make changes:

```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
git add [files you changed]
git commit -m "Description of changes"
git push origin main
```

Railway automatically redeploys when you push to GitHub!

---

## Custom Domain (Optional)

In Railway dashboard:
1. Click your project
2. Go to "Settings"
3. Click "Generate Domain" or add your own domain
4. Example: `mirrors-echo.up.railway.app`

---

## Security Notes

### Environment Variables
- Never commit .env file to GitHub (it's in .gitignore)
- Set them in Railway dashboard instead
- Railway encrypts them

### LiveKit Keys
- Your API key/secret are in Railway environment
- Users never see them
- Tokens are generated server-side

### HTTPS
- Railway provides free HTTPS automatically
- All connections are encrypted
- No certificate setup needed

---

## What Users Will See

### On Their Phone/Computer
1. Visit your Railway URL
2. See professional interface
3. Click "Start Camera" or "Join Stream"
4. No app downloads
5. Works on any device with camera/browser

### What They Experience
- Camera input goes through your TouchDesigner effects
- See themselves transformed in real-time
- Share the link with friends
- Multiple people can view simultaneously

---

## Next Steps After Deployment

### Test Everything
1. Access from your phone
2. Access from another device
3. Have a friend test it
4. Verify video quality

### Share Your Installation
- Post the URL on social media
- Include in gallery materials
- Add to your artist website
- Use QR codes at exhibitions

### Monitor Usage
- Railway dashboard shows requests/bandwidth
- LiveKit dashboard shows room activity
- Can see how many people are connected

---

## Ready to Deploy?

Run these commands now:

```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web

# Commit essential files
git add server.js package.json package-lock.json railway.json
git add publisher.html return-viewer.html index.html .gitignore
git commit -m "Ready for Railway deployment"
git push origin main

# Then go to https://railway.app and follow steps 2-5 above
```

---

**Estimated Time**: 5 minutes
**Difficulty**: Easy
**Cost**: Free (with $5 monthly credit)
**Result**: Globally accessible video installation!

Let me know when you're ready and I'll walk you through each step!
