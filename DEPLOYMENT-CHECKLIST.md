# 🚀 Railway Deployment Checklist

Quick reference checklist for deploying to Railway.

## Pre-Deployment Checklist

- [x] Node.js and npm installed (v16.0.0 or higher)
- [x] Dependencies installed (`npm install`)
- [x] WebSocket library (ws) installed
- [x] `railway.json` configuration file exists
- [x] `package.json` has correct start command
- [x] Health check passes (`./health-check.sh`)

## Deployment Steps

### 1. Railway Setup
- [ ] Accept Railway invite: https://railway.com/invite/v4BSx3LBApG
- [ ] Log into Railway dashboard
- [ ] Create or access project from invite

### 2. Deploy Backend (Signaling Server)
- [ ] Connect GitHub repository to Railway
- [ ] Deploy the project (auto-detects Node.js)
- [ ] Wait for deployment to complete
- [ ] Generate public domain in Railway settings
- [ ] Copy the Railway WebSocket URL (e.g., `wss://your-app.up.railway.app`)

### 3. Deploy Frontend (Web App)
Choose one:
- [ ] **Option A**: Deploy to GitLab Pages
  - [ ] Push code to GitLab repository
  - [ ] Wait for CI/CD pipeline to complete
  - [ ] Access at `https://username.gitlab.io/the-mirrors-echo/`
  
- [ ] **Option B**: Deploy to Vercel
  - [ ] Run `vercel` in terminal
  - [ ] Follow prompts
  
- [ ] **Option C**: Deploy to Netlify
  - [ ] Connect repository or drag-and-drop folder

### 4. Connect Frontend to Backend
- [ ] Update `config.js` with Railway WebSocket URL
  ```javascript
  window.SIGNALING_SERVER_URL = 'wss://your-app-name.up.railway.app';
  ```
- [ ] Commit and push changes
- [ ] Wait for frontend to redeploy

### 5. Testing
- [ ] Open frontend URL in browser
- [ ] Click "Start Camera" (grant permissions)
- [ ] Click "Start WebRTC Call"
- [ ] Verify "Connected to signaling server" message
- [ ] Open second browser tab/window
- [ ] Repeat camera and WebRTC steps
- [ ] Verify peer-to-peer connection established

## Verification

### Backend (Railway)
✅ Railway logs show: "WebRTC Signaling Server started on ws://localhost:XXXX"
✅ Deployment status: Active/Running
✅ Public domain generated and accessible

### Frontend
✅ Site loads without errors
✅ Camera access works
✅ WebRTC connection status shows "Connected"
✅ Console shows no error messages

### End-to-End
✅ Two browser windows can establish peer connection
✅ Video feeds appear in both windows
✅ No connection errors in Railway logs

## URLs to Track

Record your deployment URLs here:

**Railway Backend:**
- WebSocket URL: `wss://_________________.up.railway.app`
- Dashboard: https://railway.app/project/_________________

**Frontend:**
- Live URL: `https://_______________________________`
- Repository: `https://gitlab.com/kfaist/the-mirrors-echo`

## Common Issues

### Build Fails
- ✅ Check `package.json` has `ws` dependency
- ✅ Check `railway.json` configuration
- ✅ Review Railway build logs

### Connection Fails
- ✅ Use `wss://` not `ws://` or `https://`
- ✅ Verify Railway deployment is running
- ✅ Check browser console for errors

### Camera Issues
- ✅ Access via `https://` not `http://`
- ✅ Grant camera permissions
- ✅ Test locally first

## Support Resources

- **NEXT-STEPS.md**: Complete step-by-step guide
- **RAILWAY.md**: Detailed Railway deployment guide
- **README.md**: Full project documentation
- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app

## Quick Commands

```bash
# Install dependencies
npm install

# Test locally
npm run dev

# Health check
./health-check.sh

# Deploy via Railway CLI
railway login
railway link
railway up
railway domain

# View Railway logs
railway logs
```

---

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete
