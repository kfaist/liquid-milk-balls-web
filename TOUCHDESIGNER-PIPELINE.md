# 🎨 THE MIRROR'S ECHO - TouchDesigner Pipeline

Complete NDI streaming pipeline for browser → TouchDesigner → browser

---

## 📊 **COMPLETE PIPELINE**

```
User Browser (ANY device)
    ↓
mirrors-echo.html (camera + watermarks)
    ↓
OBS Browser Source (capture the page)
    ↓ NDI Output
TouchDesigner (NDI In TOP)
    ↓ Process/Effects/AI
TouchDesigner (NDI Out TOP)
    ↓
OBS (NDI Source - processed video)
    ↓ Virtual Camera OR WebRTC
User views processed return stream
```

---

## 🌐 **STEP 1: User Opens Mirror's Echo**

**URL (works on ANY browser):**
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo.html
```

**What happens:**
- ✅ Works on mobile, desktop, any browser
- ✅ User clicks "Start" → camera activates
- ✅ Temporal watermark effects start at 7 minutes
- ✅ No special setup needed for user

---

## 🎬 **STEP 2: OBS Captures Browser**

### **OBS Setup:**

1. **Add Browser Source:**
   - Source → Browser
   - URL: `https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo.html`
   - Width: `1920`
   - Height: `1080`
   - ✅ Custom CSS (optional - hide UI):
   ```css
   .intro-text, .status, footer { display: none !important; }
   .panel { padding: 0; background: transparent; border: none; }
   ```

2. **Enable NDI Output:**
   - Tools → NDI Output Settings
   - ✅ Main Output
   - Name: `OBS-MirrorsEcho`

---

## 🎨 **STEP 3: TouchDesigner Receives & Processes**

### **TD Setup:**

1. **NDI In TOP:**
   ```
   - Add: NDI In TOP
   - Source: Select "OBS-MirrorsEcho"
   - This receives the raw Mirror's Echo stream
   ```

2. **Your Processing Chain:**
   ```
   NDI In TOP
       ↓
   Your effects/filters/AI
       ↓
   NDI Out TOP
   ```

3. **NDI Out TOP:**
   ```
   - Add: NDI Out TOP
   - Source Name: "TD-Processed"
   - This sends processed video back to OBS
   ```

---

## 📺 **STEP 4: OBS Receives Processed Video**

### **Capture TD Output:**

1. **Add NDI Source:**
   - Sources → NDI Source
   - Source Name: Select "TD-Processed"
   - This shows your processed TouchDesigner output

2. **Options for Return Path:**

   **Option A: Virtual Camera (for local viewing)**
   - Tools → Virtual Camera → Start
   - User opens camera app to see processed video

   **Option B: Stream to LiveKit (for remote viewing)**
   - Use `td-publisher.html` to publish Virtual Camera
   - Remote viewers watch the processed stream

---

## 🔄 **STEP 5: User Views Processed Return**

### **For Remote Viewing:**

**Use existing return viewer:**
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html
```

**Or use td-publisher.html pipeline:**
1. Open: `https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-publisher.html`
2. Click "Start OBS Virtual Camera"
3. Click "Publish to Railway"
4. Remote viewers see processed stream

---

## 📱 **USER EXPERIENCE:**

### **What User Does:**
1. Opens `mirrors-echo.html` on phone/browser
2. Clicks "Start" → camera activates
3. Sees themselves (raw video)
4. After 7 minutes → watermarks appear
5. (Optional) Views processed return stream

### **What You Do (Behind the Scenes):**
1. OBS captures their browser stream
2. NDI → TouchDesigner processes it
3. TD → NDI → OBS gets processed video
4. Optionally stream processed video back to them

---

## ✅ **VERIFICATION CHECKLIST:**

- [ ] User can open mirrors-echo.html on ANY browser
- [ ] Camera works without special setup
- [ ] OBS captures browser source correctly
- [ ] NDI output from OBS is visible
- [ ] TouchDesigner receives NDI feed
- [ ] TD processing chain works
- [ ] TD outputs processed video via NDI
- [ ] OBS receives processed NDI feed
- [ ] User can view processed return (if needed)

---

## 🚀 **QUICK START:**

**Minimal Setup (No Return Stream):**
```
1. User → mirrors-echo.html
2. OBS → Browser Source → NDI Out
3. TD → NDI In → Process → NDI Out
4. OBS → NDI Source (display processed)
```

**Full Bidirectional Setup:**
```
1. User → mirrors-echo.html
2. OBS → Browser Source → NDI Out
3. TD → NDI In → Process → NDI Out
4. OBS → NDI Source → Virtual Camera
5. td-publisher.html → publish to web
6. User → return-viewer.html (see processed)
```

---

## 📋 **REQUIRED DEPLOYMENTS:**

All files already deployed at:
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/
```

**Available pages:**
- `/mirrors-echo.html` - Main user interface (ANY browser)
- `/td-publisher.html` - Publish OBS Virtual Cam to web
- `/return-viewer.html` - View processed return stream
- `/td-auto-viewer.html` - Alternative LiveKit viewer

---

## 🎯 **KEY POINTS:**

✅ **Browser-First:** mirrors-echo.html works on ANY browser, no plugins
✅ **NDI Pipeline:** OBS → TD → OBS via NDI (local processing)
✅ **Optional Return:** User can view processed stream if you publish it
✅ **Temporal Effects:** Watermarks activate at 7 minutes automatically
✅ **Scalable:** Works for 1 user or multiple viewers

---

**Ready to capture creativity! 🌈💧**
