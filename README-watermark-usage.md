# Watermark Dev Server Usage Guide

This guide explains how to use the no-cache development server with automatic watermark injection.

## Quick Start

### 1. Start the Server

Open PowerShell and navigate to the project directory, then start the server:

```powershell
# Navigate to project directory
cd path\to\liquid-milk-balls-web

# Start the no-cache dev server
node server_static_nocache.js
```

The server will start on port 3000 by default and display:
```
============================================================
🟢 NO-CACHE Dev Server Running
   Port: 3000
   URL: http://localhost:3000
   Cache: DISABLED (always fresh content)
============================================================
Test URLs:
   Camera Test: http://localhost:3000/simple_getusermedia.html
   Token Test: http://localhost:3000/token?identity=test
============================================================
```

### 2. Test in a Browser

Open Chrome or Firefox and navigate to:
- **Camera Test:** http://localhost:3000/simple_getusermedia.html
- **Autostart Camera:** http://localhost:3000/simple_getusermedia.html?autostart=1
- **Main App:** http://localhost:3000/index.html

You should see the rainbow droplets watermark in the bottom-right corner of any HTML page served by the server.

### 3. Test in TouchDesigner

1. Open TouchDesigner
2. Add a **Web Browser CHOP** or **Web DAT**
3. Set the URL to: `http://localhost:3000/simple_getusermedia.html?autostart=1`
4. The camera should start automatically and the watermark will be visible

## Features

### No-Cache Headers
The server forces browsers to always fetch fresh content by setting:
- `Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate`
- `Pragma: no-cache`
- `Expires: 0`

This ensures that any code changes you make are immediately visible without needing hard refresh.

### Automatic Watermark Injection
The server automatically injects a watermark into any HTML response:
- **Position:** Fixed bottom-right corner
- **Size:** 220px wide on desktop, 140px on mobile
- **Opacity:** 22% (low opacity, non-intrusive)
- **Image:** `/media/watermark.svg` (rainbow droplets with animation)

### Request Logging
All requests are logged with timestamps and user-agent info:
```
[2024-11-23T15:45:00.000Z] GET /simple_getusermedia.html
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
```

### Placeholder Token Endpoint
For testing token-based features without LiveKit:
```
http://localhost:3000/token?identity=myname
```

Returns:
```json
{
  "token": "DEV-PLACEHOLDER-TOKEN",
  "room": "claymation-live",
  "identity": "myname"
}
```

## Customization

### Change Port
Set the PORT environment variable:
```powershell
$env:PORT=8080
node server_static_nocache.js
```

### Use a PNG Watermark Instead
1. Add your PNG file to `media/watermark.png`
2. Edit `server_static_nocache.js` line 33:
   ```javascript
   // Change from:
   <img class="__site-watermark" src="/media/watermark.svg" alt="Watermark"/>
   // To:
   <img class="__site-watermark" src="/media/watermark.png" alt="Watermark"/>
   ```

### Adjust Watermark Styling
The injected CSS is in `server_static_nocache.js`. Modify the `.__site-watermark` class:
```css
.__site-watermark {
  position: fixed;
  right: 22px;      /* Distance from right edge */
  bottom: 22px;     /* Distance from bottom edge */
  width: 220px;     /* Watermark width */
  opacity: .22;     /* Transparency (0-1) */
  pointer-events: none;
  z-index: 99999;
}
```

## Troubleshooting

### "Cannot find module 'express'"
Install dependencies:
```powershell
npm install
```

### Port Already in Use
Either stop the other server or use a different port:
```powershell
$env:PORT=8080
node server_static_nocache.js
```

### Watermark Not Appearing
1. Check that `media/watermark.svg` exists
2. Open browser DevTools and check for 404 errors
3. Verify the HTML page has a `</body>` tag (required for injection)

### Camera Not Working
1. Allow camera permissions when prompted
2. Check browser console for errors
3. Ensure you're using HTTPS or localhost (required for getUserMedia)
4. Try Chrome or Firefox (best WebRTC support)

## Files Added

- `server_static_nocache.js` - The dev server
- `media/watermark.svg` - Vector watermark image
- `simple_getusermedia.html` - Camera test page
- `README-watermark-usage.md` - This file

## Production Notes

⚠️ **This server is for development only!**

- No authentication or authorization
- No rate limiting
- Verbose logging
- All files served statically

For production deployment, use the main `server.js` with proper LiveKit configuration.
