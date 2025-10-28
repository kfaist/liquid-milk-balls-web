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
