#!/bin/bash

# The Mirror's Echo - Setup Script
# This script helps set up the development environment

echo "🪞 The Mirror's Echo - Setup Script"
echo "=================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js is installed: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ npm is installed: $(npm --version)"

# Python is no longer required - we use the Node.js server
# (Keeping this comment for backwards compatibility reference)

echo ""
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Start the server: npm start"
echo "  2. Open http://localhost:3000 in your browser"
echo ""
echo "The server includes:"
echo "  • HTTP server for static files"
echo "  • WebSocket signaling for simple WebRTC (peer-to-peer)"
echo "  • LiveKit token generation (requires environment variables)"
echo ""
echo "For detailed WebRTC setup instructions, see WEBRTC-SETUP.md"
echo ""
echo "Happy coding! ✨"
