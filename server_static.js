// Dev static server with a safe /token placeholder.
// Usage: node server_static.js
// Serves files from the directory it runs in (so http://localhost:3000/simple_getusermedia.html will work).
// WARNING: This is a development helper. Do NOT use this to expose real API secrets.
// For production, use livekit_token_endpoint.js and set env LIVEKIT_API_KEY/SECRET on server.
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Simple request logger
app.use((req, res, next) => {
  console.log(new Date().toISOString(), req.method, req.url);
  next();
});

// Serve current directory as static files
app.use(express.static(path.join(__dirname, '.')));

// Placeholder /token route for dev. Replace by real token endpoint in production.
app.get('/token', (req, res) => {
  // Return a harmless placeholder so client-side code can be tested without secrets.
  res.json({
    token: 'DEV-PLACEHOLDER-TOKEN',
    room: process.env.ROOM_NAME || 'claymation-live',
    identity: req.query.identity || ('dev_user_' + Math.floor(Math.random()*100000))
  });
});

app.listen(PORT, () => {
  console.log(`Dev static server running at http://localhost:${PORT}`);
});
