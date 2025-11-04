# 🎨 PROMPT FOR NEXT CLAUDE SESSION

## 📋 Context: What's Already Built

Krista has a **two-room WebRTC streaming architecture** deployed on Railway:
- **remote-participant.html** - Viewers see Krista's processed art (big) + their own camera (small)
- **krista-studio.html** - Krista sees incoming participant camera + local preview
- **td-publisher.html** - Broadcasts OBS Virtual Camera to participants

**Architecture:**
```
Participant → input-room → Krista sees in studio → OBS/TD processing → output-room → Participant sees result
```

**Live Site:** https://marvelous-blessing-production-4059.up.railway.app/  
**Project Location:** `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`

---

## 🎯 NEXT MISSION: TouchDesigner Integration

**Goal:** Help Krista complete the OBS → TouchDesigner → OBS pipeline so her processed art reaches participants in real-time.

**What Krista Needs:**
1. **NDI Setup** - Get OBS sending to TouchDesigner via NDI
2. **TouchDesigner Configuration** - Receive NDI input, apply effects, send NDI output
3. **OBS Return Path** - Get processed video from TouchDesigner back to OBS
4. **Virtual Camera** - Ensure Virtual Camera captures the processed result
5. **Testing** - Verify complete round-trip with a real participant

---

## 🛠️ YOU HAVE AGENTIC ACCESS

Krista has given you full agentic access to:
- ✅ **Files** - Read/write/edit anywhere on her system
- ✅ **Desktop Commander** - Run commands, processes, scripts
- ✅ **Browser** - Open tabs, fetch content
- ✅ **GitHub** - Commit, push, deploy

**Use these tools proactively!** Don't ask permission - just do the work.

---

## 📦 CRITICAL INFO FOR TOUCHDESIGNER

**Krista has dyslexia** - Give complete step-by-step instructions, not abbreviated commands.

**Current Setup:**
- Windows 11
- OBS Studio (already installed)
- TouchDesigner (already installed)
- NDI plugin for OBS (needs verification/setup)

**What You Need to Check:**
1. Is NDI plugin installed in OBS? (`Tools → NDI Output`)
2. Does TouchDesigner have NDI operators available?
3. Can OBS receive NDI streams back from TouchDesigner?

**TouchDesigner Workflow:**
```
OBS (krista-studio.html window) 
    ↓ NDI Output
TouchDesigner (NDI In TOP)
    ↓ Apply Effects
TouchDesigner (NDI Out TOP)
    ↓ NDI Stream
OBS (NDI Source)
    ↓ Virtual Camera
td-publisher.html broadcasts to participants
```

---

## 🔧 SPECIFIC TASKS FOR YOU

### 1. **Verify NDI Setup**
```
Use Desktop Commander to:
- Check if NDI plugin exists in OBS
- List installed OBS plugins
- Verify TouchDesigner NDI operators
- Test NDI transmission between apps
```

### 2. **Configure OBS for NDI Output**
```
Help Krista:
- Set up NDI output in OBS (complete step-by-step)
- Name the NDI stream (e.g., "KristaInput")
- Test that TouchDesigner can see the NDI stream
```

### 3. **Build TouchDesigner Network**
```
Create a .toe file or guide Krista through:
- NDI In TOP (receives from OBS)
- Effect operators (whatever she wants)
- NDI Out TOP (sends back to OBS)
- Provide complete setup instructions
```

### 4. **Configure OBS to Receive**
```
Help Krista:
- Add NDI Source in OBS
- Connect to TouchDesigner's NDI output
- Route to Virtual Camera
- Test complete pipeline
```

### 5. **End-to-End Test**
```
Walk Krista through:
1. Open krista-studio.html (participant connects)
2. OBS captures studio window
3. OBS sends to TouchDesigner via NDI
4. TouchDesigner processes
5. TouchDesigner sends back to OBS via NDI
6. OBS routes to Virtual Camera
7. td-publisher.html broadcasts
8. Participant sees processed result
```

---

## 💡 ALTERNATIVE: LiveKit (IF WebRTC Issues)

**Only consider this if:**
- WebRTC has latency problems
- NAT traversal fails consistently  
- Krista wants more robust streaming infrastructure

**If switching to LiveKit:**
1. Set up LiveKit server (cloud or local)
2. Modify remote-participant.html to use LiveKit SDK
3. Modify td-publisher.html to publish via LiveKit
4. Update server.js if needed
5. Test thoroughly

**Note:** Current WebRTC setup is working - LiveKit is backup plan only.

---

## 📂 KEY FILES YOU'LL WORK WITH

**Web Project:**
- `C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\`
  - `krista-studio.html` - Your monitoring interface
  - `td-publisher.html` - Broadcasting interface
  - `remote-participant.html` - Viewer interface
  - `server.js` - Signaling server

**OBS Configuration:**
- Location varies, use Desktop Commander to find OBS config files
- Look for NDI plugin settings

**TouchDesigner:**
- Krista's project files (ask her for location)
- Create new .toe file if needed

---

## 🎯 SUCCESS CRITERIA

You're done when:
1. ✅ Participant connects via remote-participant.html
2. ✅ Their camera appears in krista-studio.html
3. ✅ OBS captures studio window
4. ✅ OBS sends to TouchDesigner via NDI
5. ✅ TouchDesigner applies effects (even simple test effect)
6. ✅ TouchDesigner sends back to OBS via NDI
7. ✅ OBS Virtual Camera shows processed result
8. ✅ td-publisher.html broadcasts Virtual Camera
9. ✅ Participant sees processed art in remote-participant.html
10. ✅ Latency is acceptable (< 2 seconds end-to-end)

---

## 🚨 IMPORTANT NOTES

**About Krista:**
- Dyslexia - use complete commands, not shortcuts
- Artist first, technologist second - focus on workflow not theory
- Hand hurts - you have agentic access, minimize her typing
- Prefers direct action over lengthy explanations

**Communication Style:**
- Be concise but complete
- Use step-by-step instructions
- Don't ask permission for tool use - just do it
- Create handoff docs frequently
- Use emojis for visual scanning (she likes this)

**Technical Approach:**
- Test locally before pushing to Railway
- Create backups before major changes
- Document everything in markdown files
- Use Desktop Commander proactively
- Check file locations with `read_file` before editing

---

## 📋 CHECKLIST FOR YOUR FIRST RESPONSE

When Krista starts the next session, immediately:

1. ✅ Read this prompt fully
2. ✅ Check current Railway deployment status
3. ✅ Verify OBS and TouchDesigner are installed
4. ✅ List available NDI plugins/operators
5. ✅ Ask Krista: "Ready to set up the OBS → TouchDesigner → OBS pipeline?"
6. ✅ Begin with step 1: Verify NDI Setup

---

## 🔗 USEFUL COMMANDS

**Check OBS install:**
```powershell
Get-Process obs64 -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files\obs-studio" -ErrorAction SilentlyContinue
```

**Check TouchDesigner:**
```powershell
Get-Process TouchDesigner -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files\Derivative" -Recurse -ErrorAction SilentlyContinue
```

**Find NDI Tools:**
```powershell
Get-ChildItem "C:\Program Files\NDI" -Recurse -ErrorAction SilentlyContinue
```

**List OBS plugins:**
```powershell
Get-ChildItem "C:\Program Files\obs-studio\obs-plugins" -ErrorAction SilentlyContinue
```

---

## 💾 HANDOFF DOCUMENTS ALREADY CREATED

- `STATUS-UPDATE.md` - Current deployment status
- `DEPLOYED-AND-READY.md` - User guide for web interface
- `TWO-ROOM-SETUP.md` - Technical architecture docs
- `TOUCHDESIGNER-PROMPT.md` - This file

---

## 🎨 KRISTA'S ARTISTIC VISION

She's creating "The Mirror's Echo" - an interactive AI projection installation:
- Real-time speech → visual landscapes
- Participant camera input → TouchDesigner effects → beautiful output
- Professional exhibition-quality streaming
- Seeking funding and exhibition opportunities

**Your job:** Make the technical pipeline invisible so the art can shine. ✨

---

## 🚀 LET'S GO!

When Krista says "ready" or asks about TouchDesigner, jump straight into:
1. Verifying NDI setup
2. Configuring the pipeline
3. Testing end-to-end

**You have full agentic access - use it confidently!**

Good luck! 🎨
