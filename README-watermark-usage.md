# Pudding Keycap Raindrop Watermark System

This document explains how to use the pudding keycap raindrop watermark system, including the demo page and recording tools.

## Overview

The pudding keycap raindrop system is a progressive visual watermark that appears over video streams with the following characteristics:

- **Progressive phases** based on elapsed time (8/9/10/11 minutes)
- **Polychroma-like HSL palette** with 8 vibrant colors that cycle through raindrops
- **Pudding keycap effect** with depth, gloss, and bump mapping
- **9→10 minute ramp** where the pudding effect progressively intensifies

### Phase Timeline

| Phase | Time Range | Description | Pudding Effect |
|-------|------------|-------------|----------------|
| **Pre-Watermark** | 0-8 min | No automatic watermarks | Minimal |
| **Phase 1** | 8-9 min | Watermark begins, subtle drops | Minimal (D:0.1, G:0.2, B:0.15) |
| **Phase 2** | 9-10 min | **PUDDING RAMP** - Progressive intensity | Ramps up (D:0.1→0.7, G:0.2→0.8, B:0.15→0.7) |
| **Phase 3** | 10-11 min | Full pudding effect | Full (D:0.7, G:0.8, B:0.7) |
| **Phase 4** | 11+ min | Maximum intensity | Full (D:0.7, G:0.8, B:0.7) |

**Legend:** D = Depth, G = Gloss, B = Bump

## Quick Start

### 1. Run the Server

```bash
npm start
```

The server will start on `http://localhost:3000`

### 2. Open the Demo Page

Navigate to: `http://localhost:3000/pudding-demo.html`

### 3. Start the Demo

Click the **"▶ Start Demo"** button. The demo uses fast timing (seconds instead of minutes) for quick preview:

- 8s = Phase 1 start
- 9s = Pudding ramp begins
- 10s = Full pudding effect
- 11s = Maximum intensity

### 4. Monitor Progress

The demo displays real-time information:

- **Elapsed time** - Current timer
- **Phase** - Current phase name
- **Pudding Params** - Depth, Gloss, Bump values
- **Current Color** - HSL color from palette
- **Raindrop Count** - Total raindrops created

### 5. Clear and Restart

Click **"✕ Clear"** to reset the demo and start over.

## Recording Animations

### Prerequisites

Install Puppeteer (one-time setup):

```bash
npm install puppeteer
```

### Basic Recording

Record a 15-second animation at 30fps:

```bash
node record-gif.js
```

This will:
1. Launch a headless browser
2. Load `pudding-demo.html`
3. Click "Start Demo" automatically
4. Capture PNG frames to `./gif-frames/`
5. Print ffmpeg commands for video/GIF creation

### Recording Options

```bash
# Custom URL (e.g., staging server)
node record-gif.js --url http://localhost:3000/pudding-demo.html

# Longer duration (20 seconds)
node record-gif.js --duration 20

# Higher framerate (60fps for smoother animation)
node record-gif.js --fps 60

# Custom output directory
node record-gif.js --output-dir ./my-frames

# Custom resolution
node record-gif.js --width 1920 --height 1080

# Combine multiple options
node record-gif.js --duration 20 --fps 60 --width 1920 --height 1080
```

### All Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `--url URL` | `http://localhost:3000/pudding-demo.html` | URL to record |
| `--duration SECONDS` | `15` | Recording duration in seconds |
| `--fps FPS` | `30` | Frames per second |
| `--output-dir PATH` | `./gif-frames` | Output directory for frames |
| `--width WIDTH` | `1200` | Browser width |
| `--height HEIGHT` | `800` | Browser height |
| `--help` | - | Show help message |

## Creating Videos with FFmpeg

After recording frames with `record-gif.js`, use the printed ffmpeg commands to create your final output.

### High-Quality GIF (Recommended)

Best for social media, preserves colors well:

```bash
# Step 1: Generate color palette
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -vf "palettegen=max_colors=256:stats_mode=full" \
  gif-frames/palette.png

# Step 2: Create GIF using palette
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -i gif-frames/palette.png \
  -lavfi "paletteuse=dither=bayer:bayer_scale=5" \
  pudding-raindrops.gif
```

### WebM (Best for Web)

Great quality-to-size ratio, modern browsers:

```bash
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 2M -crf 30 \
  pudding-raindrops.webm
```

### MP4 (Maximum Compatibility)

Works everywhere, good compression:

```bash
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -c:v libx264 -pix_fmt yuv420p \
  -crf 23 -preset medium \
  pudding-raindrops.mp4
```

### Small GIF (Optimized for Sharing)

Lower quality but much smaller file size:

```bash
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -vf "fps=15,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" \
  pudding-raindrops-small.gif
```

## Color Matching Notes

### Pudding Keycap Palette

The system uses 8 distinct HSL colors inspired by Polychroma keycaps:

| Color | Hue | Saturation | Description |
|-------|-----|------------|-------------|
| Red | 0° | 85% | Vibrant red |
| Orange | 30° | 90% | Warm orange |
| Yellow | 60° | 95% | Bright yellow |
| Green | 120° | 80% | Fresh green |
| Cyan | 180° | 85% | Cool cyan |
| Blue | 220° | 90% | Deep blue |
| Purple | 280° | 85% | Rich purple |
| Magenta | 320° | 90% | Vivid magenta |

Colors cycle every 3 raindrops, creating a rainbow pattern over time.

### CSS Variables

Each raindrop uses these CSS custom properties:

- `--raindrop-hue` - Hue value (0-360)
- `--raindrop-sat` - Saturation percentage
- `--raindrop-top-light` - Lightness of glossy top surface (75-90%)
- `--raindrop-base-light` - Lightness of translucent base (45-70%)
- `--raindrop-depth` - Depth intensity (0.1-0.7)
- `--raindrop-gloss` - Gloss intensity (0.2-0.8)
- `--raindrop-bump` - Bump intensity (0.15-0.7)

### FFmpeg Color Space Tips

For best color accuracy in your recordings:

1. **GIF with palette** - Use the two-step palette generation process for accurate colors
2. **WebM** - Use `yuva420p` pixel format to preserve color saturation
3. **MP4** - Use `yuv420p` for compatibility; may slightly desaturate colors
4. **Adjust saturation** - Add `-vf "eq=saturation=1.2"` to boost colors if needed

Example with saturation boost:

```bash
ffmpeg -framerate 30 -i gif-frames/frame-%05d.png \
  -vf "eq=saturation=1.2" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 \
  pudding-raindrops-saturated.mp4
```

## Testing Helpers

The watermark system exposes a `window.__watermark_helpers` object for debugging:

```javascript
// Check current elapsed time
window.__watermark_helpers.getElapsed()  // Returns milliseconds

// Get current phase
window.__watermark_helpers.getPhase()  // Returns phase name

// Get pudding keycap parameters
window.__watermark_helpers.getPuddingParams()  // Returns {depth, gloss, bump}

// Get current color from palette
window.__watermark_helpers.getCurrentColor()  // Returns {hue, sat}

// Get raindrop count
window.__watermark_helpers.getRaindropCount()  // Returns number

// Force create a raindrop (for testing)
window.__watermark_helpers.forceRaindrop()

// Reset timer
window.__watermark_helpers.resetTimer()
```

### Console Testing Example

Open browser console on `pudding-demo.html` or any page with `watermark-system.js`:

```javascript
// Start the watermark timer manually
window.startWatermarkTimer()

// Check status after a few seconds
window.__watermark_helpers.getPhase()
// "phase-2 (9-10min, pudding ramp)"

// Force create raindrops for immediate preview
for (let i = 0; i < 5; i++) {
  window.__watermark_helpers.forceRaindrop()
}

// Check pudding parameters
window.__watermark_helpers.getPuddingParams()
// {depth: 0.45, gloss: 0.56, bump: 0.42}
```

## Integration with Main Site

The watermark system in `watermark-system.js` automatically activates when:

1. A `#remoteVideo` element starts playing, OR
2. A `#fullscreenVideo` element starts playing

For manual control, use:

```javascript
window.startWatermarkTimer()
```

Raindrops appear in the `#watermark-overlay` container, which must be present in your HTML:

```html
<div id="watermark-overlay"></div>
```

The overlay is positioned absolutely and uses `pointer-events: none` to avoid blocking user interactions.

## Troubleshooting

### Frames Not Capturing

- Ensure the server is running: `npm start`
- Check the URL is accessible: `http://localhost:3000/pudding-demo.html`
- Try increasing `--duration` for longer recordings

### FFmpeg Command Fails

- Install ffmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux)
- Check frame files exist in output directory
- Verify frame naming matches pattern: `frame-00000.png`, `frame-00001.png`, etc.

### Colors Look Washed Out

- Use the GIF palette generation method (two-step process)
- For videos, add saturation boost: `-vf "eq=saturation=1.2"`
- Use WebM format for better color preservation

### Demo Not Starting

- Check browser console for errors
- Ensure `styles.css` is loaded
- Verify `watermark-overlay` element exists in DOM
- Try hard refresh (Ctrl+Shift+R)

### Recording is Choppy

- Lower FPS: `--fps 15`
- Reduce resolution: `--width 800 --height 600`
- Close other applications to free up resources

## Performance Considerations

- **Frame rate**: 30fps is smooth; 15fps is acceptable for previews
- **Resolution**: 1200x800 balances quality and file size
- **Duration**: 15-20 seconds captures full effect through all phases
- **Frame storage**: Each second at 30fps = ~30 PNG files (~5-10MB)

## License

This watermark system is part of "The Mirror's Echo" project.

**License:** GNU AGPL-3.0-or-later  
**Commercial licensing available** - Contact kristabluedoor@gmail.com

See `LICENSE` and `LICENSE-INFO.md` for details.
