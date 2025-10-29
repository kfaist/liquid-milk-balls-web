# 🚀 Your Next Steps to See a Live Site

You have a Railway invite link: **https://railway.com/invite/v4BSx3LBApG**

Follow these steps to get your site live on Railway:

## Step 1: Join the Railway Team

1. **Click your invite link**: https://railway.com/invite/v4BSx3LBApG
2. **Sign up or log in** to Railway
3. **Accept the invite** to join the team/project

## Step 2: Option A - Deploy via Railway Dashboard (Easiest)

This is the recommended approach for first-time users:

1. **Go to Railway Dashboard**: https://railway.app/dashboard
2. **Click "New Project"** or select the existing project from the invite
3. **Click "Deploy from GitHub repo"**
4. **Select this repository**: `kfaist/liquid-milk-balls-web`
5. Railway will automatically:
   - Detect the `railway.json` configuration
   - Detect the Node.js project (from `package.json`)
   - Start building and deploying
6. **Wait for deployment** (usually takes 1-2 minutes)
7. **Generate a public domain**:
   - In your Railway project, click on your service
   - Go to the **Settings** tab
   - Click **Generate Domain** under "Public Networking"
   - You'll get a URL like: `https://your-app-name.up.railway.app`

## Step 2: Option B - Deploy via Railway CLI (Advanced)

If you prefer command line:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway (opens browser)
railway login

# Link to the project from the invite
railway link

# Deploy the project
railway up

# Generate a public domain
railway domain
```

## Step 3: Test Your Deployed Signaling Server

After deployment, test if your signaling server is running:

1. **Check Railway logs**:
   - In Railway dashboard, click on your service
   - Go to the **Deployments** tab
   - Click on the latest deployment
   - View logs to confirm: "WebRTC Signaling Server started..."

2. **Test WebSocket connection**:
   ```bash
   # Replace YOUR-URL with your Railway domain
   curl -i -N -H "Connection: Upgrade" \
        -H "Upgrade: websocket" \
        -H "Sec-WebSocket-Version: 13" \
        -H "Sec-WebSocket-Key: test" \
        https://YOUR-URL.up.railway.app
   ```

## Step 4: Deploy the Web Frontend

Your signaling server is now live! Now deploy the web frontend:

### Option A: GitLab Pages (Recommended)

The repository is already configured for GitLab Pages:

1. **Create a GitLab repository** (if you haven't already):
   - Go to https://gitlab.com
   - Create a new project: `the-mirrors-echo`

2. **Push to GitLab**:
   ```bash
   git remote add gitlab https://gitlab.com/YOUR-USERNAME/the-mirrors-echo.git
   git push -u gitlab main
   ```

3. **GitLab will auto-deploy** using the `.gitlab-ci.yml` file

4. **Your site will be live** at: `https://YOUR-USERNAME.gitlab.io/the-mirrors-echo/`

### Option B: Vercel (Alternative)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Option C: Netlify (Alternative)

1. Go to https://netlify.com
2. Drag and drop your project folder
3. Or connect your GitHub repository

## Step 5: Connect Frontend to Your Railway Backend

After deploying both:

1. **Get your Railway WebSocket URL**:
   - Example: `wss://your-app-name.up.railway.app`
   - Note: Use `wss://` (secure WebSocket), not `https://`

2. **Update `config.js`**:
   ```javascript
   window.SIGNALING_SERVER_URL = 'wss://your-app-name.up.railway.app';
   ```

3. **Commit and push** the changes:
   ```bash
   git add config.js
   git commit -m "Update config with Railway WebSocket URL"
   git push
   ```

4. **Redeploy** your frontend (GitLab/Vercel/Netlify will auto-redeploy)

## Step 6: Test Everything End-to-End

1. **Open your live frontend URL** in a browser
2. **Click "Start Camera"** (grant camera permissions)
3. **Click "Start WebRTC Call"**
4. **Check the status message**: Should show "Connected to signaling server"
5. **Open a second browser tab/window** and repeat steps 2-3
6. **Verify peer connection**: Both tabs should show video feeds

## 🎉 You're Live!

Your site is now accessible from anywhere:
- **Frontend**: `https://YOUR-USERNAME.gitlab.io/the-mirrors-echo/` (or Vercel/Netlify URL)
- **Backend**: `https://your-app-name.up.railway.app`

## Troubleshooting

### "Build failed" on Railway
- Check Railway logs for error messages
- Ensure `package.json` has `ws` dependency
- Verify `railway.json` configuration

### "Can't connect to signaling server"
- Ensure Railway deployment is running (check dashboard)
- Verify you're using `wss://` (not `ws://` or `https://`)
- Check browser console for errors
- Check Railway logs for connection attempts

### Camera not working
- Ensure you're accessing via `https://` (not `http://`)
- Grant camera permissions in browser
- Test on localhost first: `npm run dev` then go to `http://localhost:8000`

## Railway Costs

Railway offers:
- **Trial**: $5 free credits initially
- **Hobby Plan**: $5/month credit (usually sufficient for this app)
- **Pro Plan**: $20/month for higher usage

Your signaling server is very lightweight and should fit within the free credits.

## Need Help?

1. Check Railway logs: `railway logs` or in dashboard
2. Check browser console for frontend errors
3. Review the full deployment guide: [RAILWAY.md](RAILWAY.md)
4. Test locally first: `npm run dev`

## Summary

**Quick checklist:**
- [ ] Accept Railway invite
- [ ] Deploy signaling server to Railway
- [ ] Get Railway WebSocket URL
- [ ] Deploy frontend to GitLab Pages/Vercel/Netlify
- [ ] Update `config.js` with Railway URL
- [ ] Test the live site

**You're ready to go! 🚀**
