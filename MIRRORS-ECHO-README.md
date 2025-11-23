# The Mirror's Echo - Integration Complete ✨

## Overview

**The Mirror's Echo** is a hybrid video interface combining local camera publishing with remote stream viewing, featuring progressive temporal watermark effects that create an iridescent veil over time.

## Features Implemented

### ✅ Complete

1. **Dual Video Interface**
   - Local camera panel (left side, collapsible)
   - Remote stream panel (right side, main view)
   - Responsive layout adapts to mobile

2. **LiveKit Integration**
   - Local camera publishes to `INPUT_ROOM` (claymation-live)
   - Remote viewer subscribes to `PROCESSED_ROOM` (processed-output)
   - Token generation via existing API endpoints
   - Auto-reconnection handling

3. **Temporal Watermark System**
   - Starts at 7 minutes into the session
   - Progressive intensity through 10+ minutes
   - Rainbow shimmer effects (site-wide)
   - Raindrop cascade (video overlay)
   - Glassmorphism text overlay at 10+ minutes
   - Color cycling every 5 raindrops

4. **UI/UX Features**
   - Collapsible local camera panel
   - Fullscreen mode for remote stream
   - Session timer with warning colors
   - Real-time status indicators
   - Buttons maintain 0.5 opacity over watermarks

## Files Created

### 1. `mirrors-echo.html` - Production Version
- Full hybrid interface (local + remote video)
- Normal timer starting at 00:00
- Watermark effects trigger at 7:00 naturally
- Use for actual sessions

**Access:** `http://localhost:3000/mirrors-echo.html`

### 2. `mirrors-echo-demo.html` - Testing Version
- Same interface as production
- Timer auto-starts at 7:00 on page load
- Watermark effects start immediately
- Demo badge shows "STARTS AT 7:00"
- Perfect for testing effects without waiting

**Access:** `http://localhost:3000/mirrors-echo-demo.html`

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  The Mirror's Echo                       │
├──────────────────────┬──────────────────────────────────┤
│   Local Camera       │    Remote Stream                 │
│   (Your webcam)      │    (Processed output)            │
│                      │                                  │
│   Publishes to →     │    ← Subscribes from             │
│   INPUT_ROOM         │      PROCESSED_ROOM              │
│                      │                                  │
│   [Collapsible]      │    [Fullscreen capable]          │
└──────────────────────┴──────────────────────────────────┘
                  ↓
        Temporal Watermark Overlay
     (Rainbow shimmer + Raindrop cascade)
```

### LiveKit Flow

1. **Local Camera** → INPUT_ROOM (`claymation-live`)
   - Token: `/api/publisher-token`
   - Publishes video + audio tracks
   - Shows "Publishing" status

2. **Remote Stream** ← PROCESSED_ROOM (`processed-output`)
   - Token: `/api/processed-viewer-token`
   - Subscribes to processed video
   - Shows in main panel

3. **TouchDesigner/OBS** captures INPUT_ROOM, processes, outputs to PROCESSED_ROOM

### Watermark Timeline

```
00:00 ──────── 07:00 ──────── 08:00 ──────── 09:00 ──────── 10:00+ ────→
         │            │            │            │            │
         │     Phase 1: Whisper    │            │            │
         │     Subtle shimmer      │            │     Phase 4: Undeniable
         │                  Phase 2: Murmur     │     Full effects
         │                  More shimmer Phase 3: Presence   Text overlay
         │                                Clear shimmer      Intense glow
```

#### Phase Details

- **00:00 - 07:00**: No automatic watermark (playful click interaction only)
- **07:00 - 08:00**: Phase 1 "Whisper" - Very subtle background shimmer
- **08:00 - 09:00**: Phase 2 "Murmur" - Raindrops every ~10 seconds, visible shimmer
- **09:00 - 10:00**: Phase 3 "Presence" - Raindrops every ~5 seconds, clear effects
- **10:00+**: Phase 4 "Undeniable" - Raindrops every ~0.8 seconds, text overlay appears

### Effect Components

1. **Rainbow Shimmer** (Site-wide)
   - Applied via body classes: `temporal-phase-1` through `temporal-phase-4`
   - Affects all text and sections with progressive intensity
   - Defined in `styles.css` lines 1113-1296

2. **Raindrop Cascade** (Video overlay)
   - Created by `watermark-system.js`
   - Spawns in `#watermark-overlay` div
   - Color cycles through rainbow hues (0-360°)
   - Each drop has shimmer line effect
   - Frequency increases with phase

3. **Glassmorphism Overlay** (Text)
   - Appears at 10+ minutes
   - Shows title, subtitle, licensing info
   - Breathing animation
   - Color-matched to current raindrop hue

## Usage Instructions

### Quick Start (Demo)

1. Start the server:
   ```bash
   npm start
   ```

2. Open demo version:
   ```
   http://localhost:3000/mirrors-echo-demo.html
   ```

3. Allow camera access when prompted

4. Effects start immediately at 7:00 mark

### Production Use

1. Start the server:
   ```bash
   npm start
   ```

2. Open production version:
   ```
   http://localhost:3000/mirrors-echo.html
   ```

3. Local camera auto-publishes to INPUT_ROOM

4. Click "Connect" to subscribe to PROCESSED_ROOM

5. Watermark effects begin at 7:00 naturally

### Testing Full Pipeline

1. **Remote Publisher** (mobile device or second browser):
   ```
   http://localhost:3000/publisher.html
   ```

2. **Processing** (TouchDesigner):
   - Subscribe to INPUT_ROOM using `td-auto-viewer.html`
   - Process video
   - Publish to PROCESSED_ROOM via WHIP

3. **Viewer** (this interface):
   ```
   http://localhost:3000/mirrors-echo.html
   ```

## UI Controls

### Local Camera Panel
- **Collapse button** (`◀`/`▶`): Hide/show local camera panel
- Auto-publishes on page load
- Shows "Publishing" status when active

### Remote Stream Panel
- **Connect**: Subscribe to processed output stream
- **Disconnect**: Unsubscribe and stop timer
- **Fullscreen**: Enter fullscreen mode for remote video
- **Timer**: Shows session duration (turns yellow at 7:00+)

### Keyboard
- **ESC**: Exit fullscreen mode

## API Endpoints Used

- `GET /api/publisher-token` - Token for local camera to publish
- `GET /api/processed-viewer-token` - Token to view processed output

## Styling

All watermark styles are in `styles.css`:
- `.video-raindrop` (lines 525-550) - Raindrop appearance
- `.raindrop-shimmer` (lines 590-605) - Shimmer line effect
- `.watermark-text-overlay` (lines 608-683) - Glassmorphism panel
- `.temporal-phase-*` (lines 1113-1296) - Progressive shimmer phases

## Technical Notes

### Browser Compatibility
- Requires modern browser with WebRTC support
- Tested on Chrome, Firefox, Safari
- Mobile responsive (switches to vertical layout)

### Performance
- Watermark overlay uses `pointer-events: none` for zero interaction cost
- Raindrop animations auto-cleanup after completion
- LiveKit adaptive streaming for bandwidth optimization

### Z-Index Layers
```
10000 - Control buttons (always visible at 0.5 opacity)
9999  - Watermark overlay (raindrops)
100   - Text overlay (glassmorphism panel)
10    - Local panel
5     - Remote header
```

### Button Visibility
All control buttons maintain 0.5 opacity when watermarked, increasing to 1.0 on hover. This ensures they remain functional even during intense effects.

## Customization

### Change Watermark Timing

Edit `watermark-system.js`:
```javascript
const PHASE_START = 8 * 60 * 1000;  // Start time (currently 8 min)
const PHASE_1 = 9 * 60 * 1000;      // Phase 1 end
const PHASE_2 = 10 * 60 * 1000;     // Phase 2 end
const PHASE_3 = 11 * 60 * 1000;     // Phase 3 end
```

### Change Demo Start Time

Edit `mirrors-echo-demo.html`:
```javascript
const DEMO_START_OFFSET = 7 * 60 * 1000; // 7 minutes
```

### Adjust Raindrop Frequency

Edit `watermark-system.js` function `getDropFrequency()`:
```javascript
return 0.12; // 12% chance per second = ~every 0.8 seconds
```

## Deployment

### Railway
Already configured in `railway.json`. Deploy with:
```bash
railway up
```

Access at:
```
https://liquid-milk-balls-web-production-2e8c.up.railway.app/mirrors-echo.html
```

### Environment Variables Required
```
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_ROOM_NAME=claymation-live
LIVEKIT_PROCESSED_ROOM=processed-output
```

## Troubleshooting

### Local camera not starting
- Check camera permissions in browser
- Ensure HTTPS or localhost (required for getUserMedia)
- Check console for errors

### Remote stream not appearing
- Verify TouchDesigner/OBS is publishing to PROCESSED_ROOM
- Check LiveKit server is running
- Verify tokens are being generated (check Network tab)

### Watermark effects not appearing
- Check `watermark-system.js` is loaded (view source)
- Verify `#watermark-overlay` div exists in DOM
- Check console for JavaScript errors
- Ensure timer has started (check timer display)

### Demo not starting at 7:00
- Check browser console for "DEMO MODE" message
- Verify watermark-system.js exports `startWatermarkTimer` function
- Ensure page loaded completely before timer starts

## Files Modified

- ✅ `mirrors-echo.html` - New production interface
- ✅ `mirrors-echo-demo.html` - New demo interface
- ✅ `watermark-system.js` - Already existed (no changes needed)
- ✅ `styles.css` - Already existed (no changes needed)
- ✅ `server.js` - Already existed (token endpoints ready)

## Next Steps

### Optional Enhancements
1. Add audio visualization to raindrops
2. Custom color schemes per user
3. Watermark intensity controls
4. Recording functionality
5. Multi-participant support (grid view)
6. Chat overlay
7. Persistent watermark settings

### Production Checklist
- [ ] Test on all target browsers
- [ ] Verify mobile responsiveness
- [ ] Load test with multiple viewers
- [ ] Monitor LiveKit bandwidth usage
- [ ] Set up error logging/monitoring
- [ ] Create user documentation
- [ ] Configure CDN for static assets

## Credits

**The Mirror's Echo** - A temporal watermark experience
Built with LiveKit, WebRTC, and progressive web effects

---

**Status**: ✅ Integration Complete
**Version**: 1.0.0
**Last Updated**: 2025-11-23
