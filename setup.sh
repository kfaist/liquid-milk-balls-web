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

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 is not installed. You'll need it to run the local web server."
    echo "   You can install it from https://www.python.org/"
else
    echo "✅ Python 3 is installed: $(python3 --version)"
fi

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
echo "  1. Start the web server: npm start"
echo "  2. In another terminal, start the signaling server: npm run signaling"
echo "  3. Open http://localhost:8000 in your browser"
echo ""
echo "Or run both servers at once: npm run dev"
echo ""
echo "Happy coding! ✨"
