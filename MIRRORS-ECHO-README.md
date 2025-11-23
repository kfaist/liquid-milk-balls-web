# 🎨 The Mirror's Echo - Temporal Watermark Integration

## Overview

The Mirror's Echo is a hybrid video interface that combines local camera and remote stream with progressive temporal watermark effects. The watermark system creates an increasingly prominent iridescent veil over time, designed as a demonstration/licensing mechanism.

## Features

### ✅ Implemented

1. **Dual Video Interface**
   - Local camera view (publishes to LiveKit)
   - Remote stream view (subscribes from LiveKit)
   - Side-by-side layout with responsive grid
   - Expand/collapse individual panels
   - Fullscreen mode for each video

2. **Progressive Temporal Watermark**
   - **7-8 minutes (Phase 1: Whisper)**: Very subtle background shimmer begins
   - **8-9 minutes (Phase 2: Murmur)**: Effects intensify, raindrops appear every 8-12 seconds
   - **9-10 minutes (Phase 3: Presence)**: Clear watermark visible, raindrops every 4-6 seconds
   - **10+ minutes (Phase 4: Undeniable)**: Full watermark with text overlay, raindrops every 0.5-1.5 seconds

3. **Visual Effects**
   - Rainbow shimmer with color cycling (changes every 5 raindrops)
   - Realistic raindrop cascade with ripple effects
   - Progressive rainbow tinting
   - Glassmorphism text overlay at 10 minutes
   - Button visibility maintained at 0.5 opacity during watermark

4. **UI/UX Features**
   - Real-time session timer display
   - Phase indicator showing current watermark stage
   - Status messages for connection events
   - Demo mode (auto-start at 7:00 for testing)
   - Clean, minimal interface

## File Structure

```
liquid-milk-balls-web/
├── mirrors-echo.html          # Main application page
├── watermark-system.js        # Temporal watermark effects logic
├── styles.css                 # Global styles including watermark CSS
└── server.js                  # LiveKit token generation endpoints
```

## How It Works

### 1. LiveKit Integration

The application uses LiveKit for real-time video streaming:

- **Publisher Role**: Publishes local camera to LiveKit room
- **Subscriber Role**: Receives remote participant's video stream
- **Token Generation**: Server-side endpoint `/api/publisher-token` generates secure access tokens

### 2. Watermark System

The watermark system (`watermark-system.js`) operates independently:

- **Trigger**: Starts when remote video begins playing
- **Timer**: Tracks elapsed session time
- **Effects**:
  - Site-wide shimmer effects via CSS classes (`temporal-phase-1` through `temporal-phase-4`)
  - Raindrop overlays created dynamically via JavaScript
  - Color cycling through rainbow spectrum
  - Text overlay with glassmorphism effect

### 3. Effect Progression

```
0-7 min    →  Normal viewing (no watermark)
7-8 min    →  Phase 1: Subtle shimmer (whisper)
8-9 min    →  Phase 2: Visible shimmer + sparse raindrops (murmur)
9-10 min   →  Phase 3: Clear watermark + frequent raindrops (presence)
10+ min    →  Phase 4: Full watermark + text overlay + constant raindrops (undeniable)
```

## Usage

### Standard Mode

1. Open `https://your-domain.com/mirrors-echo.html`
2. Click "Connect to Room"
3. Allow camera/microphone access
4. Timer starts automatically
5. Wait for remote participant to join
6. Watermark effects begin at 7 minutes

### Demo Mode

For testing watermark effects without waiting:

```
https://your-domain.com/mirrors-echo.html?demo=true
```

This auto-starts the timer at 7:00 (7 minutes), allowing you to see effects progression immediately.

## Setup Requirements

### 1. LiveKit Configuration

Set up LiveKit credentials in `.env` file:

```env
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here
LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_ROOM_NAME=mirrors-echo
```

Get these from:
- [LiveKit Cloud](https://cloud.livekit.io/) (hosted service)
- Self-hosted LiveKit server

### 2. Server Setup

The server must be running to generate LiveKit tokens:

```bash
npm install
node server.js
```

Server runs on port 3000 (or `process.env.PORT` if specified).

### 3. HTTPS Requirement

LiveKit requires HTTPS for camera access. Use one of:

- Railway deployment (automatic HTTPS)
- ngrok for local testing: `ngrok http 3000`
- Local HTTPS with self-signed cert

## API Endpoints

### Publisher Token

```
GET /api/publisher-token?identity=participant-name
```

Returns:
```json
{
  "token": "eyJhbGc...",
  "url": "wss://...",
  "room": "mirrors-echo"
}
```

### Viewer Token (optional)

```
GET /api/viewer-token?identity=viewer-name
```

Returns same format but with view-only permissions.

## Testing

### Local Testing

1. **Terminal 1**: Start server
   ```bash
   npm install
   node server.js
   ```

2. **Browser 1**: Publisher (your main browser)
   ```
   http://localhost:3000/mirrors-echo.html?demo=true
   ```

3. **Browser 2**: Remote participant (incognito/different browser)
   ```
   http://localhost:3000/publisher.html
   ```

### Production Testing

Use the deployed Railway URL:

```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo.html
```

## Customization

### Timing Configuration

Edit `watermark-system.js` to adjust phase timings:

```javascript
const PHASE_START = 7 * 60 * 1000;  // 7 minutes - watermark begins
const PHASE_1 = 8 * 60 * 1000;      // 8 minutes
const PHASE_2 = 9 * 60 * 1000;      // 9 minutes
const PHASE_3 = 10 * 60 * 1000;     // 10 minutes
```

### Raindrop Frequency

Adjust drop frequency in `getDropFrequency()` function:

```javascript
if (elapsed < PHASE_1) {
    return 0.01; // ~1% chance per second = ~every 10 seconds
}
```

### Text Overlay

Customize watermark text in `createTextOverlay()` function:

```javascript
title.textContent = "Your Custom Title";
subtitle.textContent = 'Your Subtitle';
licensing.innerHTML = 'Your licensing message';
```

## Architecture Decisions

### Why MediaStream over track.attach()?

The watermark system needs to detect the `playing` event on the `#remoteVideo` element. Using `track.attach()` creates a new video element, which would miss the event listener. Instead, we:

```javascript
remoteVideo.srcObject = new MediaStream([track.mediaStreamTrack]);
```

This ensures the watermark system can properly initialize when remote video starts.

### Why Overlay Instead of Canvas?

The watermark overlay sits above all content with `z-index: 9999` and `pointer-events: none`. This ensures:

- Watermark cannot be captured via browser screen recording
- Effects appear over fullscreen mode
- Buttons remain interactive (via higher z-index)

### Why Progressive Timing?

The 7-10 minute progression allows:

- Initial normal viewing experience
- Gradual awareness build-up
- Non-intrusive demonstration period
- Clear licensing prompt at 10+ minutes

## Troubleshooting

### Camera Not Starting

- Check HTTPS (LiveKit requires secure context)
- Verify browser permissions granted
- Check browser console for errors

### Remote Video Not Showing

- Ensure both participants connected to same room
- Check LiveKit credentials in `.env`
- Verify network allows WebRTC (some firewalls block)

### Watermark Not Appearing

- Check browser console for watermark system logs
- Verify `watermark-system.js` loaded correctly
- Ensure remote video triggered `playing` event

### Token Generation Fails

- Verify `.env` file has correct LiveKit credentials
- Check server logs for errors
- Ensure server is running and accessible

## Browser Compatibility

- ✅ Chrome/Edge 80+
- ✅ Firefox 75+
- ✅ Safari 14+
- ❌ IE (not supported)

## Performance Notes

- Raindrops are removed after animation completes (no memory leak)
- Shimmer effects use CSS animations (GPU accelerated)
- LiveKit uses adaptive streaming for bandwidth optimization
- Demo mode doesn't affect performance (just timer offset)

## License & Usage

This temporal watermark system is designed for:

- **Demo/Trial Mode**: Full experience with progressive watermark
- **Commercial Licensing**: Contact for watermark-free version
- **Exhibition License**: Time-limited commercial use

The watermark serves as both a demonstration feature and licensing prompt.

## Support & Contact

For issues, customization, or licensing inquiries:

- GitHub Issues: [kfaist/liquid-milk-balls-web](https://github.com/kfaist/liquid-milk-balls-web/issues)
- Email: Contact information in main site

---

**Created**: November 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
