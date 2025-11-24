# The Mirror's Echo

An unlimited edition networked interactive work under AGPL-3.0, exploring presence, temporality, and reciprocity through real-time video transmission and AI-driven visual processing.

## Quick Deploy to Railway

### Option 1: One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/kristafaist/mirrors-echo)

### Option 2: Via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link 440956c3-fee6-4fe9-b0a7-48bb997794a5

# Deploy
railway up
```

### Option 3: Connect GitHub Repo

1. Push these files to your GitHub repo
2. Go to [Railway Dashboard](https://railway.app/dashboard)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo - Railway auto-deploys on push

## Local Development

```bash
npm install
npm start
# Visit http://localhost:3000
```

## Features

- 🌈 Rainbow raindrops with user-controlled color influence (35-40%)
- 🎨 8-color palette with complementary slider thumbs
- 🎚️ 10 interactive parameter sliders
- ⏱️ Tempo control - accelerate or slow the 7-minute progression
- 📹 WebRTC video capture interface
- 💫 Shimmer overlays on video panels
- 📊 Temporal intensity display (peaks at 10 min, persists forever)

## Interactive Parameters

| Slider | Effect |
|--------|--------|
| **Hue** | Primary color for ~38% of drops |
| **Saturation** | Color vibrancy (0-100%) |
| **Lightness** | Brightness (0-100%) |
| **Intensity** | Opacity + spawn rate |
| **Depth** | Size variation |
| **Gloss** | Highlight shimmer |
| **Bump** | Gradient complexity |
| **Speed** | Animation speed |
| **Halo** | Glow size |
| **Tempo** | Progression speed (0.25x-4x) |

## Licensing

### Open Access (Free)
- Full source code (AGPL-3.0)
- Non-commercial use
- 7-minute unmediated experience
- Progressive temporal markers

### Exhibition License ($400)
- No temporal markers
- Commercial exhibition rights
- TouchDesigner/LiveKit integration support

### Technical Residency ($150/hour)
- Custom integration assistance
- On-site support available

### Institutional Partnership
Contact: chaoscontemporarycraft@gmail.com

## Technical Stack

- **Frontend**: Vanilla JavaScript + CSS
- **Server**: Node.js + Express
- **Protocols**: WebRTC, AGPL-3.0
- **Deployment**: Railway / Vercel / Any Node.js host

## Contact

- Artist/Technical: kristabluedoor@gmail.com
- Curatorial/Institutional: chaoscontemporarycraft@gmail.com

---

© 2025 The Mirror's Echo | Krista Faist
