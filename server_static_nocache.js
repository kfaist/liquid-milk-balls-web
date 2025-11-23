// Dev static server with NO CACHING, HTML injection for a site-wide watermark,
// and verbose request logging.
// 
// ⚠️  WARNING: FOR DEVELOPMENT USE ONLY
// This server has no authentication, rate limiting, or production security features.
// Use the main server.js for production deployments.
//
// Usage: node server_static_nocache.js
const express = require('express');
const path = require('path');
const fs = require('fs').promises;
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
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  console.log(`  User-Agent: ${String(req.headers['user-agent'] || '').substring(0, 120)}...`);
  next();
});

// Middleware: intercept HTML files and inject watermark
app.use(async (req, res, next) => {
  // Only process GET requests for HTML files
  if (req.method !== 'GET' || !req.path.endsWith('.html')) {
    return next();
  }
  
  try {
    const filePath = path.join(__dirname, req.path);
    const content = await fs.readFile(filePath, 'utf8');
    
    // Inject watermark before </body>
    if (/<\/body>/i.test(content)) {
      // Watermark injection template (inline CSS + image element)
      const watermarkHTML = `
<!-- watermark injected by server -->
<style id="__wm-style">
  .__site-watermark{
    position:fixed;
    right:22px;
    bottom:22px;
    width:220px;
    opacity:.22;
    pointer-events:none;
    z-index:99999
  }
  @media (max-width:800px){
    .__site-watermark{width:140px;right:12px;bottom:12px}
  }
</style>
<img class="__site-watermark" src="/media/watermark.svg" alt="Watermark"/>
`;
      const modifiedContent = content.replace(/<\/body>/i, watermarkHTML + '</body>');
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return res.send(modifiedContent);
    }
    
    // If no </body> tag, just send as-is
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.send(content);
    
  } catch (error) {
    // If file doesn't exist or error reading, pass to next middleware
    return next();
  }
});

// Serve current directory as static files (no caching via options)
app.use(express.static(path.join(__dirname, '.'), {
  etag: false,
  lastModified: false,
  maxAge: 0
}));

// Dev placeholder /token route (safe for local testing)
app.get('/token', (req, res) => {
  // Generate a more unique dev identity using timestamp + random
  const defaultIdentity = `dev_user_${Date.now()}_${Math.floor(Math.random()*1000)}`;
  
  res.json({
    token: 'DEV-PLACEHOLDER-TOKEN',
    room: process.env.ROOM_NAME || 'claymation-live',
    identity: req.query.identity || defaultIdentity
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
