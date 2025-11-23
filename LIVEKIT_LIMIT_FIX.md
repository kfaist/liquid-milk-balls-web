# LiveKit Free Tier Limit Exceeded - Solutions

## What Happened

You're seeing this error:
```
Error: could not establish signal connection: connection minutes limit exceeded. 
please contact the project owner.
```

This means your LiveKit free tier has run out of connection minutes for this billing period.

---

## Solution 1: Upgrade to Paid Plan (RECOMMENDED)

**Why Upgrade:**
- Unlimited connection minutes
- Better for production/gallery installations
- More concurrent participants
- Only ~$29/month

**How to Upgrade:**
1. Go to: https://cloud.livekit.io
2. Click your project: "claymation-transcription-l6e51sws"
3. Go to Billing tab
4. Choose a paid plan
5. No code changes needed - keeps same credentials!

---

## Solution 2: Create New Free Project (TEMPORARY FIX)

**Steps:**

1. **Create New Project:**
   - Visit: https://cloud.livekit.io
   - Click "New Project"
   - Name: "liquid-milk-balls-backup" (or similar)

2. **Get New Credentials:**
   - API Key: (copy from new project settings)
   - API Secret: (copy from new project settings)  
   - WebSocket URL: wss://YOUR-NEW-PROJECT.livekit.cloud

3. **Update Your .env File:**
   ```
   LIVEKIT_URL=wss://YOUR-NEW-PROJECT.livekit.cloud
   LIVEKIT_API_KEY=YOUR_NEW_API_KEY
   LIVEKIT_API_SECRET=YOUR_NEW_API_SECRET
   ```

4. **Restart Server:**
   ```bash
   # Stop current server (Ctrl+C)
   cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
   node server.js
   ```

5. **Create New WHIP Ingress:**
   ```bash
   node list_ingresses.js  # Should show empty for new project
   node configure_obs_ingress.js  # Creates new ingress with new credentials
   ```

6. **OBS Will Auto-Update:**
   The configure_obs_ingress.js script will update OBS with the new WHIP URL

---

## Solution 3: Wait for Reset

Free tier resets monthly. Check your LiveKit dashboard for reset date.

**NOT RECOMMENDED** - You probably can't wait!

---

## For Production/Gallery Use

**You MUST upgrade to paid plan because:**
- Free tier will run out during installations
- Paid plan = unlimited minutes
- Better reliability for public exhibitions
- Worth it for professional work

**Cost:** ~$29/month (way cheaper than technical failures at gallery openings!)

---

## What To Do RIGHT NOW

**Option A (Quick Test):**
Create new free project → get new credentials → update .env → restart

**Option B (Professional):**
Upgrade your existing project to paid plan → no setup changes needed

**I recommend Option B** for your gallery installations and GLEAM proposal!

---

## After You Choose

Let me know which option you pick and I'll help you:
- Update credentials if you create new project
- Verify everything works with new setup
- Test the complete INPUT + OUTPUT pipeline

**The good news:** Your OBS OUTPUT is working perfectly! We just need LiveKit minutes for the INPUT side.
