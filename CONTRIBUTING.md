# Contributing to The Mirror's Echo

Thank you for your interest in contributing to The Mirror's Echo! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **Python 3** - [Download](https://www.python.org/)
- **Git** - [Download](https://git-scm.com/)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kfaist/liquid-milk-balls-web.git
   cd liquid-milk-balls-web
   ```

2. Run the setup script (on Unix-like systems):
   ```bash
   ./setup.sh
   ```

   Or install dependencies manually:
   ```bash
   npm install
   ```

3. Start the development servers:
   ```bash
   # Terminal 1: Web server
   npm start

   # Terminal 2: Signaling server
   npm run signaling
   ```

4. Open http://localhost:8000 in your browser

## 📁 Project Structure

```
liquid-milk-balls-web/
├── index.html              # Main HTML file
├── styles.css              # Stylesheet with animations
├── script.js               # Mirror interaction logic
├── webrtc-client.js        # WebRTC client implementation
├── webrtc-signaling-server.js  # WebSocket signaling server
├── package.json            # Node.js dependencies
├── .gitlab-ci.yml          # GitLab Pages deployment config
├── setup.sh                # Setup script
└── README.md               # Project documentation
```

## 🔧 Development Guidelines

### Code Style

- Use **2 spaces** for indentation
- Use **camelCase** for JavaScript variables and functions
- Add comments for complex logic
- Keep functions small and focused

### Testing Changes

Before submitting a PR, please test:

1. **Mirror Interactions**: Click the mirror and use the "Create Echo" button
2. **WebRTC Features**: Test camera access and signaling server connection
3. **Responsive Design**: Test on different screen sizes
4. **Browser Compatibility**: Test in Chrome, Firefox, and Safari if possible

### Making Changes

1. **Fork** the repository
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** with a clear message:
   ```bash
   git commit -m "Add: Description of your changes"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Start with a verb (Add, Fix, Update, Remove, Refactor)
- Keep the first line under 50 characters
- Add detailed description if needed

Examples:
- `Add color transition animation to mirror`
- `Fix WebRTC connection timeout issue`
- `Update README with installation instructions`

## 🐛 Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title** describing the problem
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Browser and OS** information
- **Screenshots** if applicable

## 💡 Suggesting Features

Feature suggestions are welcome! Please create an issue with:

- **Clear description** of the feature
- **Use case** - why is this feature useful?
- **Proposed implementation** (if you have ideas)

## 🎨 Areas for Contribution

We welcome contributions in these areas:

### Features
- New mirror effects and animations
- Additional WebRTC features (screen sharing, recording, etc.)
- Easter eggs and interactive elements
- Accessibility improvements

### Documentation
- Tutorial videos or GIFs
- Code documentation
- Translation to other languages

### Performance
- Optimize animations
- Reduce bundle size
- Improve loading times

### Testing
- Add automated tests
- Cross-browser testing
- Mobile testing

## 🔒 Security

If you discover a security vulnerability, please email the maintainer directly instead of creating a public issue.

## 📄 License and CLA

This project uses a dual-license model:
- **AGPLv3** for open source use
- **Commercial licenses** available for proprietary use (see COMMERCIAL-LICENSE.md)

### Contributor License Agreement

**Important**: By contributing to this project, you must agree to the Contributor License Agreement (CLA) detailed in CLA.md.

The CLA allows us to:
- Distribute your contributions under AGPLv3 (open source)
- Offer commercial licenses to support the project's sustainability
- Maintain flexibility for future licensing needs

**How to sign the CLA:**
1. Read CLA.md carefully
2. Add your name to CONTRIBUTORS.md (if not already listed)
3. In your first pull request, add a comment: "I have read and agree to the CLA in CLA.md"

Your contributions will be dual-licensed under AGPLv3 and available for commercial licensing.

## 🙏 Thank You

Every contribution, no matter how small, is valuable and appreciated. Thank you for helping make The Mirror's Echo better!

## 📞 Questions?

If you have questions, feel free to:
- Create an issue with the `question` label
- Reach out to the maintainers

Happy coding! ✨
