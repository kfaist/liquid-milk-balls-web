# TOUCHDESIGNER WEBRENDER TROUBLESHOOTING

## Quick Diagnostic Steps

### Step 1: Find the WebRender Operator

**In TouchDesigner:**
1. Press **Alt+L** (opens search dialog)
2. Type: **webrender**
3. Look for operators like:
   - webrender_livekit_input
   - webRenderTOP1
   - webrender1

**Do you see it? Write down the name:** _________________

---

### Step 2: Check Operator Parameters

**Right-click the webrender operator** and select **Parameters**

**Check these settings:**

| Parameter | Should Be | Your Value |
|-----------|-----------|------------|
| Room Name | claymation-live | _______ |
| Server URL | wss://claymation-transcription-l6e51sws.livekit.cloud | _______ |
| Active | On (checked) | _______ |

---

### Step 3: Check Connection Status

**Look at the operator info** (usually shows at bottom of screen when selected)

**Check for:**
- [ ] Connected: Yes
- [ ] Participants: 1 or more
- [ ] Video Tracks: 1 or more
- [ ] Errors: None

**What do you see?** _______________________________________

---

### Step 4: Check if Publisher is Sending

**On your phone:**
1. Go to: https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html
2. Did you click "Start Camera"?
3. Did you allow camera permissions?
4. Can you see yourself in the publisher page?

- [ ] Yes, camera is working on publisher page
- [ ] No, camera is not showing

---

## Common Issues & Fixes

### Issue 1: WebRender Operator Doesn't Exist

**Solution:** You need to create it

1. In TouchDesigner, press **Tab** (operator menu)
2. Type: **webrender**
3. Select **webRenderTOP**
4. Place it in your network

Then configure with:
- Room Name: claymation-live  
- Server URL: wss://claymation-transcription-l6e51sws.livekit.cloud
- Token: (needs to be generated - I can help with this)

---

### Issue 2: WebRender Shows Black Screen

**Possible causes:**

**A. Not connected to LiveKit**
- Check Room Name is exactly: claymation-live
- Check Server URL is correct
- Look for error messages in operator info

**B. No video tracks available**
- Publisher page needs to be sending camera
- Check publisher shows your camera
- Wait a few seconds for connection

**C. Token issue**
- WebRender needs a valid LiveKit token
- Token might be expired
- Need to generate a fresh one

---

### Issue 3: Wrong Room Name

**The operator must connect to room: claymation-live**

This matches where the publisher sends camera:
- Publisher sends to: claymation-live
- WebRender receives from: claymation-live

If room names don't match, no video!

---

## Generate a Test Token

Let me create a script to generate a LiveKit token for your webrender operator:

**I'll create this next if you need it.**

---

## What to Tell Me

Please check TouchDesigner and tell me:

1. **Does the webrender operator exist?**
   - Yes / No
   - If yes, what's it called?

2. **What room name is it set to?**
   - Room Name: ___________

3. **Is it showing any errors?**
   - Error message: ___________

4. **Is the publisher page working?**
   - Can you see your camera in publisher.html? Yes / No

**Tell me what you find and I'll help fix it!**
