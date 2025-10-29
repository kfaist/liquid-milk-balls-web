# 🪞 The Mirror's Echo

An interactive web experience where reflections tell their stories.

---

## 🚀 **WANT TO SEE A LIVE SITE? START HERE!**

### 👉 **[START-HERE.md](START-HERE.md)** ← Your deployment guide

Have a Railway invite link? We've got you covered with complete step-by-step instructions!

---

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
├── index.html                  # Main HTML file
├── styles.css                  # Stylesheet with animations
├── script.js                   # Mirror interaction logic
├── webrtc-client.js           # WebRTC client implementation
├── webrtc-signaling-server.js # WebSocket signaling server
├── package.json               # Node.js dependencies and scripts
├── setup.sh                   # Automated setup script
├── .gitlab-ci.yml             # GitLab CI/CD configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guidelines
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

3. **Start the development servers**:
```bash
# Using npm scripts (recommended):
npm start              # Start web server on port 8000
npm run signaling      # Start signaling server on port 8888
npm run dev            # Start both servers at once

# Or manually:
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (if you have http-server installed)
npx http-server
```

4. Open your browser to `http://localhost:8000`

**Note**: For WebRTC features, you need to run both the web server and the signaling server.

## 🎥 Local Testing with OBS / WebRTC

The project now includes WebRTC camera preview and signaling capabilities for testing video streaming workflows with OBS and TouchDesigner.

### Quick Start

1. **Run the setup script** (one-time setup):
```bash
./setup.sh
```

2. **Start both servers**:
```bash
npm run dev
```

   Or start them separately in different terminals:
```bash
# Terminal 1
npm start

# Terminal 2
npm run signaling
```

3. **Open the web app** in your browser:
```
http://localhost:8000
```

4. **Test the WebRTC connection**:
   - Click **"Start Camera"** to access your webcam
   - Click **"Start WebRTC Call"** to connect to the signaling server
   - Open a second browser tab/window and repeat the steps to test peer-to-peer connection
   - The local video shows your camera feed, the remote video shows the peer's feed

### OBS to TouchDesigner Workflow

For streaming video from the browser to TouchDesigner via OBS and NDI:

#### Prerequisites
- **OBS Studio**: Download from [obsproject.com](https://obsproject.com/)
- **obs-ndi plugin**: Download from [obs-ndi GitHub releases](https://github.com/obs-ndi/obs-ndi/releases)
- **NDI Runtime**: Download from [ndi.tv](https://ndi.tv/tools/)

#### Steps

1. **Start the web app** (steps 1-5 above) and verify camera preview is working

2. **Configure OBS**:
   - Open OBS Studio
   - Add a new source:
     - **Option A**: Window Capture - Select your browser window
     - **Option B**: Browser Source - Enter `http://localhost:8000` as the URL
   - Crop and position the video feed as desired

3. **Enable NDI output in OBS**:
   - Go to **Tools** > **NDI Output Settings**
   - Check **"Main Output"**
   - Give it a recognizable name (e.g., "Mirror Echo WebRTC")

4. **Receive in TouchDesigner**:
   - Add an **NDI In TOP** operator
   - In the NDI In TOP parameters, select your OBS NDI source from the dropdown
   - The video feed should now appear in TouchDesigner
   - Process the stream with your preferred effects pipeline

### Signaling Server Notes

- The included `webrtc-signaling-server.js` is a **minimal relay for local testing only**
- It is **not secure** and should not be deployed to production
- For local testing, it relays WebRTC signaling messages (SDP offers/answers and ICE candidates) between peers
- The WebRTC client uses Google's public STUN server (`stun:stun.l.google.com:19302`)
- For production or non-local testing, add TURN servers for NAT traversal

### Troubleshooting

- **Camera not accessible**: Ensure you're using `http://localhost` (not `file://`) and grant camera permissions
- **Signaling server connection fails**: Check that `node webrtc-signaling-server.js` is running and port 8888 is available
- **NDI source not visible in TouchDesigner**: Verify NDI Runtime is installed and OBS NDI output is enabled
- **Video quality issues**: Adjust camera constraints in `webrtc-client.js` or OBS output settings

## 🚀 Deploy to Railway (Remote Access)

To use WebRTC from anywhere (not just localhost), deploy the signaling server to Railway:

### Quick Deploy

**🎯 NEW: Complete Deployment Guides Available!**

- **[START-HERE.md](START-HERE.md)** - Overview and quick navigation
- **[NEXT-STEPS.md](NEXT-STEPS.md)** - Step-by-step walkthrough (recommended)
- **[DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md)** - Quick reference checklist
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details

**Quick validation:** Run `./railway-readiness-check.sh` before deploying

### Railway CLI Quick Start

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

📖 **Full guides:** 
- Detailed walkthrough: [NEXT-STEPS.md](NEXT-STEPS.md)
- Railway specifics: [RAILWAY.md](RAILWAY.md)
- Quick checklist: [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md)

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
