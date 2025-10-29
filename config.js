// Configuration for WebRTC Signaling Server
// Update this after deploying to Railway with your deployment URL

// Replace with your Railway deployment URL
// Example: 'wss://your-app-name.up.railway.app'
window.SIGNALING_SERVER_URL = 'ws://localhost:8888';

// For production deployment:
// 1. Deploy webrtc-signaling-server.js to Railway
// 2. Get your Railway public URL (e.g., https://your-app.up.railway.app)
// 3. Update the URL above to use wss:// instead of https://
//    (e.g., 'wss://your-app.up.railway.app')
// 4. Save and commit this file
