# 🪞 The Mirror's Echo

An interactive web experience where reflections tell their stories.

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
the-mirrors-echo/
├── index.html          # Main HTML file
├── styles.css          # Stylesheet with animations
├── script.js           # Interactive JavaScript
├── .gitlab-ci.yml      # GitLab CI/CD configuration
└── README.md           # This file
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
git clone https://gitlab.com/kfaist/the-mirrors-echo.git
cd the-mirrors-echo
```

2. Open with a local server (recommended):
```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (if you have http-server installed)
npx http-server
```

3. Open your browser to `http://localhost:8000`

Or simply open `index.html` directly in your browser.

## 🎥 Local Testing with OBS / WebRTC

The project now includes WebRTC camera preview and signaling capabilities for testing video streaming workflows with OBS and TouchDesigner.

### Quick Start

1. **Start a local web server** (required for camera access):
```bash
python -m http.server 8000
```

2. **Install WebSocket dependency** (one-time setup):
```bash
npm install ws
```

3. **Start the signaling server**:
```bash
node webrtc-signaling-server.js
```

4. **Open the web app** in your browser:
```
http://localhost:8000
```

5. **Test the WebRTC connection**:
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

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues or questions:
- Open an issue on GitLab
- Check the GitLab Pages documentation: https://docs.gitlab.com/ee/user/project/pages/

---

**Made with ✨ for GitLab Pages**

Deployed at: https://kfaist.gitlab.io/the-mirrors-echo/
