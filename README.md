# 🪞 The Mirror's Echo

An interactive web experience where reflections tell their stories.

## 📄 License

This project is licensed under the **GNU AGPL-3.0-or-later**. Commercial licensing is available; see [LICENSE-INFO.md](LICENSE-INFO.md) or contact kristabluedoor@gmail.com.

For full license details, see the [LICENSE](LICENSE) file.

## 🌟 About

The Mirror's Echo is a mesmerizing interactive website featuring:
- **Interactive Mirror**: Click to create ripples and echoes
- **Dynamic Messages**: Discover different reflections with each interaction
- **Responsive Design**: Works beautifully on all devices
- **Easter Eggs**: Hidden surprises await the curious
- **Modern Design**: Glassmorphism effects with smooth animations

## 🚀 Deployment to GitLab Pages

### Prerequisites
- A GitLab account
- Git installed on your local machine

### Step-by-Step Deployment

#### 1. Create a New GitLab Repository

1. Go to [GitLab](https://gitlab.com)
2. Click **New Project/Repository**
3. Choose **Create blank project**
4. Set project name: `the-mirrors-echo`
5. Set project slug: `the-mirrors-echo`
6. Set visibility level (Public, Internal, or Private)
7. **Uncheck** "Initialize repository with a README"
8. Click **Create project**

#### 2. Push Code to GitLab

```bash
# Clone this repository or navigate to your local copy
cd /path/to/the-mirrors-echo

# Add GitLab as a remote (replace USERNAME with your GitLab username)
git remote add gitlab https://gitlab.com/kfaist/the-mirrors-echo.git

# Or if you want to replace the origin:
# git remote set-url origin https://gitlab.com/kfaist/the-mirrors-echo.git

# Push to GitLab
git push -u gitlab main

# If your default branch is 'master' instead of 'main':
# git push -u gitlab master
```

#### 3. GitLab Pages Automatic Deployment

Once you push your code, GitLab CI/CD will automatically:
1. Detect the `.gitlab-ci.yml` file
2. Run the deployment pipeline
3. Deploy your site to GitLab Pages

You can monitor the deployment:
1. Go to your GitLab project
2. Click **CI/CD** > **Pipelines**
3. Watch the pipeline run

#### 4. Access Your Deployed Site

After successful deployment, your site will be available at:
```
https://kfaist.gitlab.io/the-mirrors-echo/
```

Or for custom domains:
```
https://USERNAME.gitlab.io/the-mirrors-echo/
```

### 🔧 Configuration Notes

- The `.gitlab-ci.yml` file is configured to deploy from the `main` or `master` branch
- All static files (HTML, CSS, JS) are copied to the `public` directory
- GitLab Pages serves content from the `public` directory by default

## 📁 Project Structure

```
liquid-milk-balls-web/
├── index.html                  # Main HTML file with simple WebRTC
├── ndi-viewer.html            # LiveKit viewer page
├── styles.css                  # Stylesheet with animations
├── script.js                   # Mirror interaction logic
├── webrtc-client.js           # Simple WebRTC client implementation
├── server.js                   # Main server (HTTP + WebSocket + LiveKit)
├── webrtc-signaling-server.js # Legacy standalone signaling (optional)
├── config.js                   # WebSocket URL configuration
├── package.json               # Node.js dependencies and scripts
├── .gitlab-ci.yml             # GitLab CI/CD configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # License file
├── WEBRTC-SETUP.md            # Complete WebRTC setup guide
└── README.md                  # This file
```

## 🎮 Features & Interactions

### Basic Interactions
- **Click the Mirror**: Create ripples and change the echo message
- **Create Echo Button**: Generate multiple ripples at once
- **Clear Button**: Reset the mirror to its original state

### Advanced Features
- **Progressive Color Changes**: The mirror changes color every 5 echoes
- **Ambient Animation**: Subtle breathing effect when echoes are active
- **Konami Code Easter Egg**: Try the classic code! ⬆️⬆️⬇️⬇️⬅️➡️⬅️➡️BA

## 🛠️ Local Development

To run locally:

1. Clone the repository:
```bash
git clone https://github.com/kfaist/liquid-milk-balls-web.git
cd liquid-milk-balls-web
```

2. **Quick setup** (on Unix-like systems):
```bash
./setup.sh
```

   Or **manual setup**:
```bash
npm install
```

3. **Start the development server**:
```bash
npm start              # Start unified server on port 3000
```

4. Open your browser to `http://localhost:3000`

**Note**: The server includes both HTTP serving and WebSocket signaling for WebRTC in a single process.

## 🎥 WebRTC Setup - Two Options

The project supports **two WebRTC modes** for different use cases:

### Option 1: Simple WebRTC (Peer-to-Peer)
Best for local testing and development without external services.

#### Quick Start

1. **Install dependencies** (one-time setup):
```bash
npm install
```

2. **Start the server**:
```bash
npm start
```

3. **Open the web app** in your browser:
```
http://localhost:3000
```

4. **Test Simple WebRTC (Peer-to-Peer)**:
   - Open `http://localhost:3000` in your browser
   - Click **"Start Camera"** to access your webcam
   - Click **"Start WebRTC Call"** to connect to the signaling server
   - Open a second browser tab/window and repeat the steps to test peer-to-peer connection
   - The local video shows your camera feed, the remote video shows the peer's feed

### Option 2: LiveKit (Production-Ready)
Best for scalable streaming with multiple viewers and production deployments.

#### Setup LiveKit

1. **Get LiveKit credentials**:
   - Sign up at [LiveKit Cloud](https://livekit.io) or self-host LiveKit server
   - Get your API Key, API Secret, and WebSocket URL

2. **Configure environment variables**:
```bash
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"
export LIVEKIT_URL="wss://your-project.livekit.cloud"
export LIVEKIT_ROOM_NAME="claymation-live"  # Optional, defaults to 'claymation-live'
```

3. **Start the server**:
```bash
npm start
```

4. **Test LiveKit streaming**:
   - **Publisher**: Use OBS with LiveKit WHIP output or the LiveKit SDK
   - **Viewer**: Open `http://localhost:3000/ndi-viewer.html` in your browser
   - Click "Join Live Stream" to view the published stream

### Complete Setup Guide

For detailed instructions on WebRTC setup, NDI/OBS integration, and troubleshooting, see:

📖 **[WEBRTC-SETUP.md](WEBRTC-SETUP.md)** - Complete WebRTC and NDI/OBS integration guide

Quick summary:
1. Install OBS Studio, obs-ndi plugin, and NDI Runtime
2. Start your WebRTC session (either mode)
3. Capture browser in OBS (Window Capture or Browser Source)
4. Enable NDI output in OBS (Tools → NDI Output Settings)
5. Receive in TouchDesigner with NDI In TOP operator

### WebRTC Architecture Notes

**Simple WebRTC (Peer-to-Peer)**:
- The server includes a WebSocket endpoint at `/ws` for signaling
- This is a **minimal relay for local testing only** and is **not secure**
- It relays WebRTC signaling messages (SDP offers/answers and ICE candidates) between peers
- Uses Google's public STUN server (`stun:stun.l.google.com:19302`)
- For production peer-to-peer, add TURN servers for NAT traversal
- Best for: Local testing, simple peer-to-peer connections

**LiveKit**:
- Uses LiveKit Cloud or self-hosted LiveKit server for signaling and media routing
- Production-ready with built-in TURN servers and media routing
- Supports multiple publishers and subscribers
- Scalable to hundreds of participants
- Best for: Production deployments, NDI streaming, multiple viewers

### Troubleshooting

- **Camera not accessible**: Ensure you're using `http://localhost` (not `file://`) and grant camera permissions
- **Signaling server connection fails**: Check that `npm start` is running and the server is listening on port 3000
- **LiveKit viewer shows error**: Verify environment variables are set correctly (LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL)
- **NDI source not visible in TouchDesigner**: Verify NDI Runtime is installed and OBS NDI output is enabled
- **Video quality issues**: Adjust camera constraints in `webrtc-client.js` or OBS output settings

## 🚀 Deploy to Railway (Remote Access)

To use WebRTC from anywhere (not just localhost), deploy the signaling server to Railway:

### Quick Deploy

1. **Deploy to Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

2. **Get your deployment URL:**
   ```bash
   railway domain
   ```
   Example: `https://your-app.up.railway.app`

3. **Update configuration:**
   Edit `config.js` and set:
   ```javascript
   window.SIGNALING_SERVER_URL = 'wss://your-app.up.railway.app';
   ```

4. **Deploy the web app:**
   - Push to GitLab for automatic Pages deployment, or
   - Deploy to Vercel/Netlify/GitHub Pages

📖 **Full guide:** See [RAILWAY.md](RAILWAY.md) for detailed deployment instructions

**Benefits:**
- ✅ Access from any device/location
- ✅ Share with others via public URL
- ✅ Free tier available ($5 credit/month)
- ✅ Automatic HTTPS/WSS encryption

## 📱 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🎨 Customization

Feel free to customize:
- **Colors**: Modify the gradient in `styles.css`
- **Messages**: Edit the `echoMessages` array in `script.js`
- **Animations**: Adjust timing and effects in both CSS and JS files

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Development setup and workflow
- Code style guidelines
- How to submit pull requests
- Reporting bugs and suggesting features

Quick start for contributors:
1. Fork the repository
2. Run `./setup.sh` to set up your environment
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes and test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Open an issue on GitHub/GitLab
- Check the [CONTRIBUTING.md](CONTRIBUTING.md) for common questions
- GitLab Pages documentation: https://docs.gitlab.com/ee/user/project/pages/

---

**Made with ✨ for GitLab Pages**

Deployed at: https://kfaist.gitlab.io/the-mirrors-echo/
