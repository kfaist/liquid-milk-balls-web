# 🚨 FIX: "VideoInput Failed" Error

**Error:** "starting videoinput failed"
**Location:** Railway publisher.html page
**Cause:** Camera permissions or conflict

---

## ✅ QUICK FIX #1: Use Localhost Instead (RECOMMENDED)

**The Railway version might have permission issues. Use your LOCAL version instead:**

1. **Open this URL in Firefox:**
   ```
   http://localhost:3000/publisher.html
   ```

2. **Click "Start Camera"**

3. **Grant permissions when browser asks**

4. **Success!** Local version works better for testing

---

## ✅ QUICK FIX #2: Check if OBS is Using Camera

**OBS might be blocking the camera!**

1. **Go to OBS Studio**
2. **Look for "Video Capture Device" source**
3. **Right-click it → Properties**
4. **Change "Device" to "Deactivate"** (temporarily)
5. **Try publisher.html again**

---

## ✅ QUICK FIX #3: Browser Permissions

**Firefox might be blocking camera:**

1. **Click the lock icon** (left of URL bar)
2. **Find "Camera" permission**
3. **Set to "Allow"**
4. **Refresh page (F5)**
5. **Try "Start Camera" again**

---

## 🎯 RECOMMENDED SOLUTION

**For now, use LOCALHOST for testing:**

**Publisher (Input):**
```
http://localhost:3000/publisher.html
```

**Viewer (Output):**
```
http://localhost:3000/return-viewer.html
```

**Why:** 
- No HTTPS permission issues
- Easier camera access
- Better for local testing
- Railway is for public sharing later

---

## 📱 WHEN TO USE RAILWAY

**Use Railway URLs when:**
- Sharing with remote participants
- Public installations
- Testing from phone/tablet
- After camera permissions are sorted

**For now:** Stick with localhost:3000 for testing!

---

## 🔧 IF STILL HAVING ISSUES

**Check what's using camera:**

1. Close OBS (if not needed right now)
2. Close any video call apps (Zoom, Teams, Skype)
3. Close other browser tabs with camera access
4. Try again with localhost:3000

---

**Quick test now:** http://localhost:3000/publisher.html
