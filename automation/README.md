# Automation Scripts - Liquid Milk Balls Pipeline

This folder contains automation scripts to simplify starting your video processing pipeline.

---

## 📜 Available Scripts

### 1. **START_COMPLETE_PIPELINE.ps1** (Recommended)
**Main startup script that launches everything in order.**

**Usage:**
```powershell
.\START_COMPLETE_PIPELINE.ps1
```

**What it does:**
- Starts Node.js server on port 3000
- Guides you through starting TouchDesigner
- Launches OBS Studio
- Prompts you to click "Start Streaming"
- Verifies everything is working

**Options:**
```powershell
# Skip certain components
.\START_COMPLETE_PIPELINE.ps1 -SkipServer
.\START_COMPLETE_PIPELINE.ps1 -SkipTouchDesigner
.\START_COMPLETE_PIPELINE.ps1 -SkipOBS
```

---

### 2. **auto_start_obs.py**
**Python script to automate OBS streaming.**

**Requirements:**
```bash
pip install pyautogui psutil pillow
```

**Usage:**
```bash
python auto_start_obs.py
```

**What it does:**
- Launches OBS if not running
- Waits for OBS to fully load
- Attempts to click "Start Streaming" button
- Uses image recognition OR keyboard shortcuts

**Configuration:**
To use image recognition, take a screenshot of the "Start Streaming" button and save as `start_streaming_button.png` in this folder.

---

### 3. **start_obs_streaming.ahk**
**AutoHotkey script for Windows automation.**

**Requirements:**
- Download and install AutoHotkey from https://www.autohotkey.com

**Usage:**
```
Right-click → Run Script
```

**What it does:**
- Waits for OBS to be running
- Activates OBS window
- Sends keyboard commands to start streaming

**Note:** You may need to set a hotkey in OBS first:
- File → Settings → Hotkeys
- Find "Start Streaming"
- Set hotkey (e.g., F9)

---

### 4. **setup_and_start.ps1**
**Advanced PowerShell script that configures OBS hotkeys.**

**Usage:**
```powershell
.\setup_and_start.ps1
```

**What it does:**
- Adds F9 hotkey for "Start Streaming" in OBS config
- Launches OBS
- Sends F9 keypress to start streaming automatically

**Note:** OBS must be closed when running this script to modify config.

---

## 🎯 Which Script Should You Use?

### For Daily Use
**Use:** `START_COMPLETE_PIPELINE.ps1`

This is the most reliable all-in-one solution that guides you through each step.

### For Full Automation
**Choose one of these:**

1. **setup_and_start.ps1** - Best for Windows, modifies OBS config
2. **auto_start_obs.py** - Best if you're comfortable with Python
3. **start_obs_streaming.ahk** - Best if you prefer AutoHotkey

---

## 🔧 Troubleshooting

### "Execution of scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python script can't find button
- Take screenshot of "Start Streaming" button
- Save as `start_streaming_button.png` in automation folder
- Or set OBS hotkey and use keyboard method

### AutoHotkey script doesn't work
- Check OBS has focus (window is active)
- Adjust sleep timers if OBS loads slowly
- Set manual hotkey in OBS settings

---

## 📝 Manual Alternative

If all automation fails, follow this sequence:

1. Open PowerShell:
   ```powershell
   cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
   node server.js
   ```

2. Open TouchDesigner and load your project

3. Open OBS Studio

4. Click "Start Streaming" in OBS

**This always works!** Automation is for convenience.

---

## 🎨 Customization

### Change OBS Hotkey
Edit `setup_and_start.ps1`:
```powershell
# Change this line:
"OBS_KEY_F9"
# To your preferred key, e.g.:
"OBS_KEY_F10"
```

### Change Server Port
Edit `START_COMPLETE_PIPELINE.ps1`:
```powershell
# Find this line:
Get-NetTCPConnection -LocalPort 3000
# Change 3000 to your port
```

### Adjust Timing
All scripts have `Start-Sleep` or `time.sleep()` commands.
Increase these values if your computer is slow:
```powershell
Start-Sleep -Seconds 5  # Increase to 10 if needed
```

---

## ⚙️ Advanced: OBS WebSocket

For the most reliable automation, enable OBS WebSocket:

1. Open OBS
2. Tools → WebSocket Server Settings
3. ☑ Enable WebSocket server
4. Port: 4455
5. Password: (leave empty)
6. Click OK

Then use the existing WebSocket script:
```bash
cd ..
python obs_start_stream.py
```

This allows programmatic control of OBS without GUI automation.

---

## 📞 Getting Help

**If automation isn't working:**
1. Check OBS logs: `%APPDATA%\obs-studio\logs`
2. Run scripts from PowerShell to see error messages
3. Fall back to manual startup (always works)

**For technical issues:**
- Check `SOLUTION_COMPLETE.md` in parent folder
- Review `QUICK_START.md` for troubleshooting

---

**Created:** November 22, 2025
**Purpose:** Simplify daily operation of video processing pipeline
