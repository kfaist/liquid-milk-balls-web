# 🎥 LIQUID MILK BALLS - INPUT PIPELINE SETUP GUIDE

## 🎯 WHAT YOU HAVE NOW

✅ **Server Running** - Node.js server on localhost:3000  
✅ **LiveKit Configured** - Connected to claymation-transcription-l6e51sws.livekit.cloud  
✅ **HTML Pages Created** - Publisher, TD Viewer, Status Dashboard  
✅ **Auto-Setup Script** - master_setup.py for TouchDesigner  
✅ **Testing Tools** - Multiple diagnostic pages and scripts  

## 🚀 QUICK START (3 STEPS)

### 1. OPEN STATUS DASHBOARD
```
http://localhost:3000/status-dashboard.html
```
- Click "CHECK SERVER" - should show ONLINE
- Click "CONNECT TO LIVEKIT" - should show CONNECTED
- Keep this page open for monitoring

### 2. START PUBLISHER
```
http://localhost:3000/publisher.html
```
- Allow camera access
- Click "Start Publishing"
- Should see yourself and "Publishing" status
- Dashboard should show "1 publisher"

### 3. CONFIGURE TOUCHDESIGNER
Open TouchDesigner textport (Alt+T) and run:
```
execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/master_setup.py')
```

This will:
- Find or create a Web Client TOP
- Set URL to http://localhost:3000/td-input-viewer.html
- Configure resolution (1920x1080)
- Enable audio
- Reload the page

**LOOK AT THE WEB CLIENT TOP - YOU SHOULD SEE VIDEO!**

## 📁 IMPORTANT FILES

### HTML Pages
- **publisher.html** - Remote camera publishing page
- **td-input-viewer.html** - Viewer page for Web Client TOP
- **status-dashboard.html** - Real-time pipeline monitoring
- **livekit-test.html** - Connection diagnostic tool
- **return-viewer.html** - View processed output from OBS

### Python Scripts (for TouchDesigner)
- **master_setup.py** - AUTO-CONFIGURE Web Client TOP (USE THIS!)
- **auto_config_webclient.py** - Alternative setup script
- **check_webclient_tops.py** - Diagnostic for existing TOPs

### Node.js Scripts
- **server.js** - Main server (already running)
- **test-pipeline.js** - Test all components
- **.env** - LiveKit configuration

### Documentation
- **QUICK-REFERENCE.txt** - Quick command reference
- **README.md** - This file

## 🔧 MANUAL CONFIGURATION

If you prefer to configure the Web Client TOP manually:

1. **Create or Select Web Client TOP** in TouchDesigner

2. **Set Parameters:**
   - URL: `http://localhost:3000/td-input-viewer.html`
   - Resolution W: `1920`
   - Resolution H: `1080`
   - Audio: `on`
   - Active: `True`

3. **Click Reload** parameter to refresh the page

## 📊 MONITORING & DEBUGGING

### Status Dashboard (RECOMMENDED)
Open: `http://localhost:3000/status-dashboard.html`

This shows:
- Server status
- LiveKit connection
- Number of publishers
- Active video/audio tracks
- Real-time event log

### LiveKit Test Page
Open: `http://localhost:3000/livekit-test.html`

Detailed connection diagnostic with:
- Connection state
- Room information
- Participant list
- Track subscriptions
- Console logs

### Test Pipeline Script
Run: `node test-pipeline.js`

Tests:
- Server health
- Token generation
- HTML file availability

## 🐛 TROUBLESHOOTING

### Problem: No video in Web Client TOP

**Check List:**
1. Is server running? → Check status dashboard
2. Is publisher connected? → Dashboard shows participant count
3. Is Web Client TOP URL correct? → Should be `http://localhost:3000/td-input-viewer.html`
4. Try clicking Reload parameter on Web Client TOP
5. Check browser console (F12) for errors

**Solutions:**
- Run master_setup.py again in TouchDesigner
- Restart publisher page
- Check that publisher says "Publishing" not "Not Publishing"

### Problem: Publisher won't connect

**Check List:**
1. Server running? → Should see "✅ Server running on port 3000"
2. Camera permission granted?
3. Browser console errors?

**Solutions:**
- Refresh publisher page
- Check browser console (F12)
- Try different browser (Chrome/Firefox)

### Problem: Server won't start (EADDRINUSE)

**Solution:**
```powershell
Get-NetTCPConnection -LocalPort 3000 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}
```
Wait 2 seconds, then `node server.js`

### Problem: "Connection state: Disconnected"

**Check List:**
1. LiveKit credentials in .env correct?
2. Internet connection working?
3. Firewall blocking WebSocket?

**Solutions:**
- Check .env file has correct LIVEKIT_URL, API_KEY, API_SECRET
- Test with livekit-test.html
- Check firewall settings

## 🎬 HOW IT WORKS

### The Pipeline Flow

```
Remote Browser (Publisher)
    ↓ [Camera Stream]
    ↓ [WebRTC via LiveKit]
LiveKit Cloud (claymation-live room)
    ↓ [WebRTC Subscription]
td-input-viewer.html in Web Client TOP
    ↓ [Video Element]
TouchDesigner Web Client TOP
    ↓ [TOP Output]
Your Effects and Processing
```

### Key Components

1. **Publisher (publisher.html)**
   - Captures camera from remote browser
   - Publishes to LiveKit room "claymation-live"
   - Uses /api/publisher-token for authentication

2. **TD Input Viewer (td-input-viewer.html)**
   - Subscribes to LiveKit room "claymation-live"
   - Displays incoming video full-screen
   - Auto-connects on page load
   - Uses /api/viewer-token for authentication

3. **Web Client TOP (TouchDesigner)**
   - Loads td-input-viewer.html
   - Renders the webpage as a texture
   - Outputs video for processing

4. **LiveKit Cloud**
   - WebRTC media server
   - Handles all video routing
   - Room: claymation-live

## 📝 LIVEKIT CONFIGURATION

From .env file:
```
LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

## 🎯 TESTING CHECKLIST

Before calling it "working", verify all these:

- [ ] Server starts without errors
- [ ] test-pipeline.js shows all tests PASS
- [ ] Publisher page loads and shows camera
- [ ] Publisher successfully publishes (shows "Publishing")
- [ ] Status dashboard shows 1 publisher when publishing
- [ ] Status dashboard shows video tracks when publishing
- [ ] td-input-viewer.html shows video when opened directly
- [ ] Web Client TOP URL is correct
- [ ] Web Client TOP shows video from publisher
- [ ] Video updates in real-time
- [ ] Can disconnect/reconnect publisher and it still works

## 🎨 NEXT STEPS AFTER IT WORKS

Once you see video in the Web Client TOP:

1. **Connect to Effects**
   - Route Web Client TOP output to your effects chain
   - Add your visual processing
   - Output to NDI for OBS

2. **Global Distribution**
   - OBS receives NDI from TouchDesigner
   - OBS streams via WHIP to LiveKit
   - return-viewer.html shows processed output globally

3. **Multiple Publishers**
   - Test with multiple browser tabs
   - Each gets a unique participant ID
   - All appear in the same LiveKit room

## 💡 PRO TIPS

1. **Keep Status Dashboard Open**
   - Real-time monitoring of entire pipeline
   - See exactly when things connect/disconnect
   - Event log shows what's happening

2. **Use master_setup.py**
   - Fastest way to configure TouchDesigner
   - Handles all parameter settings
   - Forces page reload

3. **Test Incrementally**
   - First: Verify server works
   - Second: Verify publisher works
   - Third: Verify LiveKit connection
   - Fourth: Configure TouchDesigner
   - Fifth: Check video appears

4. **Browser Console is Your Friend**
   - F12 opens developer console
   - Check for JavaScript errors
   - See LiveKit connection logs
   - Verify track subscriptions

## 🆘 STILL NOT WORKING?

If you've tried everything:

1. **Capture Screenshots**
   - Status dashboard showing connection state
   - Publisher page showing status
   - TouchDesigner Web Client TOP parameters
   - Browser console showing any errors

2. **Check These Specific Things**
   - Web Client TOP URL parameter (exact match required)
   - Publisher shows "Publishing" in green
   - Status dashboard shows "1" publisher
   - Browser console has no red errors
   - Server console shows no errors

3. **Try This Recovery Sequence**
   ```
   1. Stop server (Ctrl+C)
   2. Kill port 3000 (command in troubleshooting)
   3. Close all browser tabs
   4. Restart server: node server.js
   5. Open status dashboard
   6. Click "CONNECT TO LIVEKIT"
   7. Open publisher, allow camera, start publishing
   8. Run master_setup.py in TouchDesigner
   9. Check Web Client TOP
   ```

## 📞 READY TO TEST!

Everything is set up and ready to go. Follow the QUICK START section and you should see video!

The status dashboard at `http://localhost:3000/status-dashboard.html` will guide you through the process and show exactly what's working and what isn't.

**LET'S GET IT WORKING! 🚀**
