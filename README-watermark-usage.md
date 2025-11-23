# No-cache dev server + watermark

This adds a small development static server that injects an animated SVG watermark into served HTML pages and provides a getUserMedia test page.

**⚠️ FOR LOCAL DEVELOPMENT ONLY - NOT FOR PRODUCTION USE**

This server is designed for local testing and development with no security measures (no rate limiting, no authentication). Only use on your local machine.

Quick start (PowerShell):

```powershell
cd "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web"
# install deps if needed
npm install express
# start server
node server_static_nocache.js
```

Open in browser:
- http://localhost:3000/simple_getusermedia.html?autostart=1

TouchDesigner notes:
- Set WebRender TOP URL to the same page and ensure Enable Media Stream is On.
- If TD CEF permissions block getUserMedia, set a writable User Cache Directory and restart the TOP (we discussed steps in the thread).
