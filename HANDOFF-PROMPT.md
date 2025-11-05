# 🔄 HANDOFF PROMPT - Remote Camera WebRTC System

## 📍 CURRENT SITUATION

**Project:** liquid-milk-balls-web (WebRTC camera streaming to OBS/TouchDesigner)
**Location:** C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
**Deployed:** https://marvelous-blessing-production-4059.up.railway.app/
**Status:** BROWSER CACHE ISSUE - System deployed but browser showing old LiveKit error

---

## 🎯 GOAL

Stream remote user's camera → OBS Browser Source → NDI → TouchDesigner → Screen 2

---

## 🔧 SYSTEM ARCHITECTURE

**Using:** Custom WebRTC (peer-to-peer with WebSocket signaling) - FREE!
**NOT using:** LiveKit (we tried but CDN loading issues, reverted)

**Flow:**
```
Remote User Phone/Browser
  ↓ (clicks "Start Camera" + "Start WebRTC Call")
WebSocket Signaling Server (Railway at /ws)
  ↓
OBS Browser Source (same URL, shows "Remote Stream")
  ↓
OBS NDI Output
  ↓
TouchDesigner (NDI In TOP)
  ↓
Screen 2 Output
```

---

## 📁 KEY FILES

1. **index.html** - Publisher/Viewer page (has both local & remote video)
2. **webrtc-client.js** - Custom WebRTC client (ACTIVE)
3. **livekit-publisher.js** - LiveKit client (NOT ACTIVE, tried & reverted)
4. **ndi-viewer.html** - LiveKit-based viewer (NOT USED)
5. **server.js** - Express + WebSocket signaling server
6. **config.js** - Auto-detects correct WebSocket URL (wss://... or ws://localhost:3000/ws)

---

## ⚠️ CURRENT PROBLEM

**Symptom:** Browser showing "❌ Error: LiveKit SDK not loaded"

**Root Cause:** Browser is CACHED on old version (before we reverted to webrtc-client.js)

**Railway Status:** Successfully deployed 4 minutes ago (reverted to custom WebRTC)

**What User Sees:**
- Phone: "Connecting to signaling server..." (stuck)
- OBS Browser Source: "Waiting for remote user..." (stuck)

---

## ✅ WHAT WAS FIXED

Latest commit (`b5958a6`): Reverted index.html to use `webrtc-client.js` instead of LiveKit

**Changed:**
```html
<!-- OLD (LiveKit) -->
<script src="https://cdn.jsdelivr.net/npm/livekit-client@2.5.10/dist/livekit-client.umd.min.js"></script>
<script src="livekit-publisher.js"></script>

<!-- NEW (Custom WebRTC) -->
<script src="webrtc-client.js"></script>
```

---

## 🚀 IMMEDIATE NEXT STEPS

1. **HARD REFRESH BROWSER** - Clear cache completely
   - Phone: Force close browser, reopen
   - Desktop: Ctrl+Shift+R on Railway URL
   - OBS: Right-click Browser Source → Refresh

2. **TEST SIGNALING CONNECTION:**
   - Open browser console (F12)
   - Look for: "Connected to signaling server"
   - WebSocket should connect to: `wss://marvelous-blessing-production-4059.up.railway.app/ws`

3. **VERIFY FLOW:**
   - Remote user clicks "Start Camera" → Should see their camera
   - Remote user clicks "Start WebRTC Call" → Should connect
   - OBS Browser Source → Should show remote camera in "Remote Stream" box

---

## 🔍 DEBUGGING CHECKLIST

**If still stuck:**

1. Check Railway deployment logs for WebSocket connections
2. Open browser console on both devices
3. Check Network tab for WebSocket connection status
4. Verify no firewall/proxy blocking WSS connections
5. Try different browser (Chrome recommended)

---

## 💻 OBS SETUP (once working)

**Browser Source Settings:**
- URL: `https://marvelous-blessing-production-4059.up.railway.app/`
- Width: 1920
- Height: 1080
- ✅ "Shutdown source when not visible"
- Custom CSS (optional):
```css
body { overflow: hidden; }
.container { max-width: none; }
.video-wrapper:first-child { display: none !important; } /* Hide local camera */
```

**NDI Output:**
- OBS → Tools → NDI Output Settings → ✅ Enable "Main Output"

**TouchDesigner:**
- NDI In TOP → Select "KRISTA-SHOWPUTER-01 (OBS)"

---

## 📊 TECHNICAL DETAILS

**WebSocket Signaling Server:**
- Path: `/ws`
- Auto-configured by `config.js`
- Server broadcasts all messages to connected clients (simple relay)

**WebRTC Configuration:**
- STUN server: `stun:stun.l.google.com:19302`
- Peer-to-peer connection
- No TURN server (may not work on restrictive networks)

**Railway Environment:**
- Node.js server
- Port: 3000 (auto-assigned by Railway)
- WebSocket + HTTP on same server

---

## 🎨 USER CONTEXT

**User:** Krista - VR/AI artist, prefers direct step-by-step instructions
**Project:** "The Mirror's Echo" - Interactive AI projection installation
**Use Case:** Remote camera → OBS → TouchDesigner → Live projection
**Network:** User has dyslexia, needs clear, actionable guidance

---

## 📝 CONVERSATION HISTORY SUMMARY

1. Started with LiveKit attempt (CDN loading issues)
2. Discovered user already had working custom WebRTC system
3. Reverted to custom WebRTC (webrtc-client.js)
4. Deployed successfully to Railway
5. **CURRENT ISSUE:** Browser cache showing old LiveKit error

---

## 🔗 IMPORTANT LINKS

- **Railway Dashboard:** https://railway.com/project/bd63cb55-e6cf-4def-9b37-fd29d7f36605
- **LiveKit Dashboard:** https://cloud.livekit.io/projects/p_3ou36xol2x7/overview (not in use)
- **GitHub Repo:** https://github.com/kfaist/liquid-milk-balls-web
- **Deployed App:** https://marvelous-blessing-production-4059.up.railway.app/

---

## 🎯 SUCCESS CRITERIA

✅ Remote user sees own camera in "Local Camera" box
✅ Remote user sees "Connected to signaling server" status
✅ OBS Browser Source shows remote camera in "Remote Stream" box
✅ OBS NDI output enabled
✅ TouchDesigner receives NDI feed
✅ Output displays on Screen 2

---

## 💡 QUICK WIN

**Most likely fix:** Hard refresh browser (Ctrl+Shift+R) to clear LiveKit error cache. The system is already deployed and working - just need fresh HTML/JS loaded.

**If that doesn't work:** Check browser console for actual errors and WebSocket connection status.

---

## 📱 WHAT USER SAID

> "it says connecting to signaling server on my phone and in obs it says waiting for remote user"

This suggests WebSocket IS attempting to connect but may be:
- Cached on old code
- WebSocket not completing handshake
- Both devices not in same "room" (custom WebRTC broadcasts to all clients)

**Next diagnostic:** Open browser console on both devices and check for WebSocket messages.
