#!/bin/bash

# The Mirror's Echo - Health Check Script
# Verifies that the environment is properly configured

echo "🪞 The Mirror's Echo - Health Check"
echo "===================================="
echo ""

EXIT_CODE=0

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js: Not installed"
    EXIT_CODE=1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm: $NPM_VERSION"
else
    echo "❌ npm: Not installed"
    EXIT_CODE=1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python 3: $PYTHON_VERSION"
else
    echo "⚠️  Python 3: Not installed (optional, but recommended for web server)"
fi

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✅ Dependencies: Installed"
else
    echo "⚠️  Dependencies: Not installed (run 'npm install' or './setup.sh')"
fi

# Check if ws package is installed
if [ -d "node_modules/ws" ]; then
    WS_VERSION=$(node -p "require('./node_modules/ws/package.json').version" 2>/dev/null)
    echo "✅ WebSocket library (ws): $WS_VERSION"
else
    echo "⚠️  WebSocket library (ws): Not installed"
fi

# Check if ports are available
if command -v lsof &> /dev/null; then
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port 8000: In use (web server port)"
    else
        echo "✅ Port 8000: Available"
    fi
    
    if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port 8888: In use (signaling server port)"
    else
        echo "✅ Port 8888: Available"
    fi
else
    echo "ℹ️  Port check: Skipped (lsof not available)"
fi

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "🎉 Environment is ready!"
    echo ""
    echo "To start the application:"
    echo "  npm run dev      # Start both servers"
    echo "  npm start        # Start only web server"
    echo "  npm run signaling # Start only signaling server"
else
    echo "❌ Environment needs setup"
    echo ""
    echo "Please install the missing dependencies:"
    echo "  Node.js: https://nodejs.org/"
    echo "  npm: Comes with Node.js"
    echo ""
    echo "Then run: ./setup.sh"
fi

exit $EXIT_CODE
