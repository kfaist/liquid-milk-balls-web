# Railway Deployment Troubleshooting Guide

This guide helps resolve common Railway deployment issues for the liquid-milk-balls-web project.

## Quick Health Check

Before troubleshooting, verify the repository state:

```bash
# 1. Check npm installation works
npm ci

# 2. Validate dependencies
npm run validate

# 3. Test server locally
npm start
# Visit http://localhost:3000/healthz (should return "ok")
```

## Common Issues & Solutions

### 1. npm ci Fails - Package Lock Mismatch

**Symptoms:**
```
npm ERR! `npm ci` can only install packages when your package.json and package-lock.json are in sync.
```

**Causes:**
- package.json and package-lock.json are out of sync
- Merge conflicts corrupted the lockfile
- Manual edits to package-lock.json

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Regenerate lockfile from package.json
npm install

# Commit the new lockfile
git add package-lock.json
git commit -m "Regenerate package-lock.json"
git push
```

### 2. Missing Dependencies (express, ws, livekit-server-sdk)

**Symptoms:**
```
Error: Cannot find module 'express'
Error: Cannot find module 'ws'
```

**Causes:**
- Dependencies not listed in package.json
- npm ci failed silently
- node_modules accidentally committed and causing conflicts

**Solution:**
```bash
# Verify dependencies are in package.json
cat package.json | grep -A 5 "dependencies"

# Should show:
# "express": "^4.21.1",
# "ws": "^8.18.0",
# "livekit-server-sdk": "^2.0.0"

# If missing, add them:
npm install express@^4.21.1 ws@^8.18.0 livekit-server-sdk@^2.0.0

# Commit changes
git add package.json package-lock.json
git commit -m "Fix missing dependencies"
git push
```

### 3. Git Push Fails - Remote Changes Conflict

**Symptoms:**
```
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

**Causes:**
- Local branch is behind remote
- Merge conflicts from other contributors
- Railway made commits (though unlikely)

**Solution:**
```bash
# Fetch latest changes
git fetch origin

# Check what changed remotely
git log HEAD..origin/main --oneline

# Merge or rebase
git pull --rebase origin main

# Resolve any conflicts, then:
git add .
git rebase --continue

# Push changes
git push origin main
```

### 4. Railway Not Auto-Deploying

**Symptoms:**
- Git push succeeds but Railway doesn't deploy
- No new deployment appears in Railway dashboard

**Causes:**
- Railway GitHub integration disconnected
- Wrong branch configured in Railway
- Railway service paused/suspended

**Solution:**

#### Check Railway Settings:
1. Go to Railway dashboard → Your project
2. Click on your service
3. Go to Settings → Source
4. Verify:
   - **Repository**: `kfaist/liquid-milk-balls-web`
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: `/` (or blank)

#### Re-link GitHub Integration:
1. Settings → Source → Disconnect
2. Connect → GitHub
3. Select `kfaist/liquid-milk-balls-web` repository
4. Select `main` branch
5. Click "Deploy"

#### Manual Deploy:
If auto-deploy is stuck, trigger manually:
```bash
# Option 1: Via Railway CLI
railway up

# Option 2: Via Dashboard
# Go to Deployments → Click "Deploy" button
```

### 5. Node/npm Version Mismatch

**Symptoms:**
```
npm ERR! engine Unsupported engine
npm ERR! Required: {"node":">=18.0.0","npm":">=7.0.0"}
```

**Causes:**
- Railway using outdated Node.js/npm version
- Engine specification too strict

**Solution:**

The package.json already specifies minimum versions:
```json
"engines": {
  "node": ">=18.0.0",
  "npm": ">=7.0.0"
}
```

Railway (via Nixpacks) should automatically use Node 18+. If issues persist:

1. Check Railway deployment logs for actual Node/npm version
2. Add `.node-version` file to specify exact version:
   ```bash
   echo "20" > .node-version
   git add .node-version
   git commit -m "Pin Node version for Railway"
   git push
   ```

### 6. Build Succeeds But Server Fails to Start

**Symptoms:**
```
Build: ✅ Success
Deploy: ❌ Failed
Error: Server crashed on startup
```

**Causes:**
- PORT environment variable not set
- Missing environment variables for LiveKit
- Server.js syntax errors

**Solution:**

#### Check Railway Environment Variables:
1. Go to Settings → Variables
2. Verify Railway provides `PORT` (should be automatic)
3. For LiveKit (optional):
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
   - `LIVEKIT_URL`
   - `LIVEKIT_ROOM_NAME` (optional, defaults to 'claymation-live')

#### Test Locally:
```bash
# Start server with custom port
PORT=8080 node server.js

# Check if it listens correctly
curl http://localhost:8080/healthz
```

#### Check Logs:
```bash
# Via Railway CLI
railway logs

# Or in Railway dashboard → Deployments → View logs
```

### 7. Health Check Failing

**Symptoms:**
```
Deploy failed: Health check timeout
GET /healthz returned 502/503/504
```

**Causes:**
- Server not binding to 0.0.0.0
- Health check endpoint not responding
- Server crashed after startup

**Solution:**

Verify server.js listens on all interfaces:
```javascript
server.listen(PORT, "0.0.0.0", () => {
  console.log(`[server] HTTP+WS listening on :${PORT}`);
});
```

This is already configured correctly in server.js.

Test health check locally:
```bash
npm start &
sleep 2
curl http://localhost:3000/healthz
# Should return: ok
```

## Railway Configuration Reference

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "node server.js",
    "healthcheckPath": "/healthz",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### package.json Requirements
```json
{
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "build": "npm ci --prefer-offline --no-audit",
    "validate": "node --version && npm --version && npm ls"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=7.0.0"
  },
  "dependencies": {
    "ws": "^8.18.0",
    "express": "^4.21.1",
    "livekit-server-sdk": "^2.0.0"
  }
}
```

## Prevention Best Practices

### Before Pushing:
```bash
# 1. Run validation
npm run validate

# 2. Test server locally
npm start
# Visit http://localhost:3000/healthz

# 3. Check git status
git status

# 4. Verify no unwanted files
git diff --cached

# 5. Push to GitHub
git push origin main
```

### Regular Maintenance:
```bash
# Keep dependencies up to date (periodically)
npm update

# Audit for security vulnerabilities
npm audit

# Clean install to verify lockfile integrity
rm -rf node_modules
npm ci
```

### Git Workflow:
1. Always pull before making changes: `git pull origin main`
2. Make small, focused commits
3. Test locally before pushing
4. Keep package.json and package-lock.json in sync
5. Never commit node_modules (already in .gitignore)

## Getting Help

### Check Railway Status:
- Railway Status: https://status.railway.app/
- Railway Logs: `railway logs` or Dashboard → Deployments → Logs

### Debug Locally:
```bash
# Enable verbose npm output
npm ci --loglevel verbose

# Test server with debugging
DEBUG=* node server.js
```

### Useful Railway CLI Commands:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Deploy manually
railway up

# Check status
railway status

# Open project in browser
railway open
```

## Contact & Support

If issues persist:
1. Check Railway deployment logs for specific errors
2. Review GitHub Actions (if configured)
3. Check Railway dashboard for service health
4. Review this troubleshooting guide
5. Contact repository maintainer

## Changelog

- 2025-11-04: Initial troubleshooting guide created
- Added npm engine specifications to package.json
- Added validation and build scripts
- Documented common Railway deployment issues and solutions
