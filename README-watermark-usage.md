# Pudding Keycap Raindrops - Watermark System Usage

## Overview

The pudding keycap raindrops are translucent, satin-ribbon-like visual effects that appear over your video content during live sessions. They gradually increase in depth, gloss, and bump characteristics between 9-10 minutes, creating an increasingly noticeable presence.

## Quick Start

### 1. Preview the Effect

Open the demo page to see the effect in action with accelerated timing:

```bash
# Start the server
npm start

# Open in browser
open http://localhost:3000/pudding-demo.html
```

The demo uses seconds instead of minutes for rapid preview:
- **5-10s**: Whisper phase (subtle hints)
- **10-15s**: THE PUDDING RAMP - depth/gloss/bump gradually increase
- **15-20s**: Presence phase (stabilized high values)
- **20s+**: Undeniable phase (maximum effect)

### 2. Integration

The watermark system is automatically active in production pages. It uses:

- `watermark-system.js` - Core timing and raindrop creation logic
- `styles.css` - Pudding keycap CSS styles
- `#watermark-overlay` - Required HTML element for raindrop container

Key timing phases (production):
- **8-9 min**: Loss of control begins (every 8-12 seconds)
- **9-10 min**: THE PUDDING RAMP - increasing depth/gloss/bump
- **10-11 min**: Stabilized presence (every 2-3 seconds)
- **11+ min**: Cannot be ignored (every 0.5-1.5 seconds)

## Recording Demos

### Prerequisites

Install Puppeteer (if not already installed):

```bash
npm install puppeteer
# or add to package.json devDependencies:
# "puppeteer": "^21.0.0"
```

### Capture Frames

Use the recording helper script to capture PNG frames:

```bash
# Basic usage (25s at 30fps)
node record-gif.js

# Custom URL, duration, and framerate
node record-gif.js http://localhost:3000/pudding-demo.html 30 24

# Different page
node record-gif.js http://localhost:3000/index.html 60 30
```

**Parameters:**
- `url` - Target page URL (default: `http://localhost:3000/pudding-demo.html`)
- `duration` - Recording duration in seconds (default: 25)
- `fps` - Frames per second (default: 30)

Frames are saved to `./frames/frame_00000.png` through `frame_NNNNN.png`

### Encoding Videos

After capturing frames, use the provided ffmpeg commands to encode:

#### High-Quality GIF (Optimized, ~2-5MB)

```bash
ffmpeg -framerate 30 -i ./frames/frame_%05d.png \
  -vf "fps=30,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 pudding-keycaps.gif
```

#### WebM (Best for Web, ~500KB-2MB)

```bash
ffmpeg -framerate 30 -i ./frames/frame_%05d.png \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 2M -auto-alt-ref 0 \
  pudding-keycaps.webm
```

#### MP4 (Universal, ~1-3MB)

```bash
ffmpeg -framerate 30 -i ./frames/frame_%05d.png \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  pudding-keycaps.mp4
```

#### MP4 with Alpha/Transparency (HEVC)

```bash
ffmpeg -framerate 30 -i ./frames/frame_%05d.png \
  -c:v libx265 -preset slow -crf 18 -pix_fmt yuva420p -tag:v hvc1 \
  pudding-keycaps-alpha.mp4
```

#### Smaller GIF (Reduced Quality, ~500KB-1MB)

```bash
ffmpeg -framerate 30 -i ./frames/frame_%05d.png \
  -vf "fps=15,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" \
  -loop 0 pudding-keycaps-small.gif
```

### Encoding Tips

**Quality vs File Size:**
- Adjust `-crf` (18-28): Lower = better quality, larger file
- Adjust `-b:v` (500K-5M): Higher = better quality, larger file
- Use `-preset slow` for better compression (slower encoding)

**Resolution:**
- Social media: `scale=600:-1` or `scale=800:-1`
- Documentation: `scale=1200:-1` or `scale=1600:-1`
- Full HD: `scale=1920:-1`

**Frame Rate:**
- Smooth: 30 fps
- Standard: 24 fps
- Efficient: 15 fps (GIFs)

**Loop Control:**
- Infinite loop: `-loop 0` (GIF)
- Play once: `-loop -1` (GIF)
- N times: `-loop N` (GIF)

## Color Matching

To match colors from a sample photo/video:

### 1. Extract Color Palette

Use an online tool or image editor to identify the dominant hue:
- Open your sample photo in an image editor
- Use color picker to get HSL values
- Note the Hue value (0-360)

### 2. Update CSS Variables

Edit the raindrop hue in your HTML or CSS:

**In pudding-demo.html:**
```css
.video-raindrop {
    --raindrop-hue: 200;  /* Change this value (0-360) */
    --raindrop-intensity: 0.3;  /* Brightness (0-1) */
}
```

**In styles.css (for production):**
```javascript
// In watermark-system.js, update getCurrentHue():
function getCurrentHue() {
    const baseHue = 200;  // Your custom base hue
    return (baseHue + Math.floor(raindropCount / 5) * 30) % 360;
}
```

### 3. Test and Adjust

- Start with your extracted hue value
- Adjust `--raindrop-intensity` for brightness (0.2-0.6)
- Adjust `--gloss` multiplier in CSS for shine (0.3-1.0)
- Reload the demo page and re-record

### Common Color Ranges

- **Blue-Purple**: 200-280
- **Pink-Magenta**: 280-340
- **Red-Orange**: 0-30
- **Yellow-Green**: 60-120
- **Cyan-Blue**: 180-240

## Technical Details

### Pudding Keycap Effect

The "pudding keycap" aesthetic comes from:

1. **Translucent layers**: Multiple semi-transparent gradients
2. **Satin finish**: Subtle gloss effect (not mirror-bright)
3. **Depth effect**: CSS variables control 3D appearance
4. **Bump mapping**: Border and shadow effects simulate texture

### CSS Variables

Set by JavaScript for each raindrop:

```css
--depth: 0.3-2.0     /* 3D depth effect */
--gloss: 0.3-1.0     /* Surface glossiness */
--bump: 0.5-2.0      /* Texture/bump intensity */
--raindrop-hue: 0-360        /* Color hue */
--raindrop-intensity: 0-1    /* Overall opacity */
```

### The 9-10 Minute Ramp

During production playback (9-10 minutes):
- `depth` increases from 0.5 → 2.0
- `gloss` increases from 0.3 → 1.0
- `bump` increases from 0.5 → 2.0

This creates the signature "pudding keycap" look that stabilizes after 10 minutes.

## Use Cases

### Portfolio & Documentation
- Capture 25-30 second clips showing the progression
- Encode as WebM or MP4 for best quality
- Use 1200px+ width for detail

### Social Media
- 15-20 second clips at 600-800px width
- GIF for Twitter/Reddit (optimize for <5MB)
- MP4 for Instagram/TikTok (best compression)

### Project Showcases
- Record full progression (60+ seconds)
- Multiple angles/compositions
- WebM with alpha for overlay compositing

## Troubleshooting

### Recording Issues

**"Puppeteer not found"**
```bash
npm install puppeteer
```

**"Cannot connect to URL"**
- Ensure server is running: `npm start`
- Check URL is correct: `http://localhost:3000/pudding-demo.html`
- Try with different port if 3000 is in use

**Frames are blank/black**
- Increase wait time in script (line: `await page.waitForTimeout(1000)`)
- Check page has `#watermark-overlay` element
- Verify demo auto-starts or click start button

### Encoding Issues

**"ffmpeg not found"**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

**File size too large**
- Reduce resolution: `scale=600:-1`
- Lower frame rate: `-framerate 15`
- Increase compression: `-crf 23` (MP4) or reduce palette colors (GIF)

**Colors look wrong**
- Check source frames are correct
- Adjust `-pix_fmt` (yuv420p, yuva420p)
- Review palettegen settings for GIFs

## License

GNU AGPL-3.0-or-later

Commercial licensing available - contact kristabluedoor@gmail.com

---

**Questions or Issues?** Open an issue on the repository or contact the maintainer.
