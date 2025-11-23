// Dev static server with NO CACHING and better logging
// Usage: node server_static_nocache.js
// This version forces browsers to always fetch fresh content
const express = require('express');
const path = require('path');
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
  console.log(`  User-Agent: ${req.headers['user-agent']?.substring(0, 50)}...`);
  next();
});

// Serve current directory as static files
app.use(express.static(path.join(__dirname, '.'), {
  etag: false,
  lastModified: false,
  maxAge: 0
}));

// Placeholder /token route for dev
app.get('/token', (req, res) => {
  res.json({
    token: 'DEV-PLACEHOLDER-TOKEN',
    room: process.env.ROOM_NAME || 'claymation-live',
    identity: req.query.identity || ('dev_user_' + Math.floor(Math.random()*100000))
  });
});

app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log(`🟢 NO-CACHE Dev Server Running`);
  console.log(`   Port: ${PORT}`);
  console.log(`   URL: http://localhost:${PORT}`);
  console.log(`   Cache: DISABLED (always fresh content)`);
  console.log('='.repeat(60));
  console.log('\nTest URLs:');
  console.log(`   Camera Test: http://localhost:${PORT}/simple_getusermedia.html`);
  console.log(`   Token Test: http://localhost:${PORT}/token?identity=test`);
  console.log('='.repeat(60));
});
