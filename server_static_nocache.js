// Dev static server with NO CACHING, HTML injection for a site-wide watermark,
// and verbose request logging.
// Usage: node server_static_nocache.js
const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3000;

// NO-CACHE HEADERS - Forces fresh content every time
app.use((req, res, next) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  next();
});

// Enhanced request logger
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  const userAgent = String(req.headers['user-agent'] || '');
  const truncated = userAgent.length > 120 ? userAgent.substring(0, 120) + '...' : userAgent;
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  console.log(`  User-Agent: ${truncated}`);
  next();
});

// Custom static file handler that injects watermark into HTML files
app.use((req, res, next) => {
  // Only handle .html files
  if (!req.url.endsWith('.html') && !req.url.endsWith('.htm')) {
    return next();
  }
  
  const filePath = path.join(__dirname, req.url);
  
  // Check if file exists
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return next(); // File not found, let express.static handle it
    }
    
    try {
      // Inject watermark before </body>
      if (/<\/body>/i.test(data)) {
        const watermarkHTML = `\n<!-- watermark injected by server -->\n<style id="__wm-style">\n  .__site-watermark{position:fixed;right:22px;bottom:22px;width:220px;opacity:.22;pointer-events:none;z-index:99999} \n  @media (max-width:800px){ .__site-watermark{width:140px;right:12px;bottom:12px} }\n</style>\n<img class="__site-watermark" src="/media/watermark.svg" alt="Watermark"/>\n`;
        data = data.replace(/<\/body>/i, watermarkHTML + '</body>');
      }
      
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      res.send(data);
    } catch (e) {
      console.error('watermark-inject error', e);
      res.send(data); // Send original if error
    }
  });
});

// Serve current directory as static files (no caching via options)
app.use(express.static(path.join(__dirname, '.'), {
  etag: false,
  lastModified: false,
  maxAge: 0
}));

// Dev placeholder /token route (safe for local testing)
const MAX_RANDOM_USER_ID = 100000;

app.get('/token', (req, res) => {
  res.json({
    token: 'DEV-PLACEHOLDER-TOKEN',
    room: process.env.ROOM_NAME || 'claymation-live',
    identity: req.query.identity || ('dev_user_' + Math.floor(Math.random() * MAX_RANDOM_USER_ID))
  });
});

app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log(`🟢 NO-CACHE Dev Server Running`);
  console.log(`   Port: ${PORT}`);
  console.log(`   URL: http://localhost:${PORT}`);
  console.log(`   Cache: DISABLED (always fresh content)`);
  console.log('='.repeat(60));
  console.log('Test URLs:');
  console.log(`   Camera Test: http://localhost:${PORT}/simple_getusermedia.html`);
  console.log(`   Token Test: http://localhost:${PORT}/token?identity=test`);
  console.log('='.repeat(60));
});
