#!/bin/bash

# Quick validation script for Railway deployment readiness
# Run this before deploying to ensure everything is configured correctly

echo "🚀 Railway Deployment Readiness Check"
echo "======================================"
echo ""

EXIT_CODE=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Node.js
echo "📦 Checking prerequisites..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"
else
    echo -e "${RED}❌ Node.js: Not installed${NC}"
    EXIT_CODE=1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm: $NPM_VERSION${NC}"
else
    echo -e "${RED}❌ npm: Not installed${NC}"
    EXIT_CODE=1
fi

echo ""
echo "📋 Checking project files..."

# Check required files
REQUIRED_FILES=(
    "webrtc-signaling-server.js"
    "package.json"
    "railway.json"
    "index.html"
    "config.js"
    "NEXT-STEPS.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
    else
        echo -e "${RED}❌ $file missing${NC}"
        EXIT_CODE=1
    fi
done

echo ""
echo "🔍 Checking package.json configuration..."

# Check if ws dependency exists
if grep -q '"ws"' package.json; then
    echo -e "${GREEN}✅ WebSocket (ws) dependency defined${NC}"
else
    echo -e "${RED}❌ WebSocket (ws) dependency missing${NC}"
    EXIT_CODE=1
fi

# Check start command
if grep -q '"start".*"node webrtc-signaling-server.js"' package.json; then
    echo -e "${GREEN}✅ Start command configured${NC}"
else
    echo -e "${YELLOW}⚠️  Start command might be misconfigured${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check node version requirement
if grep -q '"node".*">=16' package.json; then
    echo -e "${GREEN}✅ Node.js version requirement set${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js version requirement not set${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "🔍 Checking railway.json configuration..."

if [ -f "railway.json" ]; then
    if grep -q '"startCommand".*"node webrtc-signaling-server.js"' railway.json; then
        echo -e "${GREEN}✅ Railway start command configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Railway start command might be misconfigured${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}❌ railway.json missing${NC}"
    EXIT_CODE=1
fi

echo ""
echo "📦 Checking dependencies..."

if [ -d "node_modules" ]; then
    if [ -d "node_modules/ws" ]; then
        WS_VERSION=$(node -p "require('./node_modules/ws/package.json').version" 2>/dev/null)
        echo -e "${GREEN}✅ Dependencies installed (ws: $WS_VERSION)${NC}"
    else
        echo -e "${RED}❌ ws package not installed${NC}"
        echo "   Run: npm install"
        EXIT_CODE=1
    fi
else
    echo -e "${RED}❌ Dependencies not installed${NC}"
    echo "   Run: npm install"
    EXIT_CODE=1
fi

echo ""
echo "⚙️  Checking configuration..."

if grep -q "ws://localhost:8888" config.js; then
    echo -e "${YELLOW}⚠️  config.js still uses localhost (OK for local testing)${NC}"
    echo "   Update to Railway URL after deployment"
    WARNINGS=$((WARNINGS + 1))
elif grep -q "wss://" config.js; then
    RAILWAY_URL=$(grep -o 'wss://[^'"'"']*' config.js | head -1)
    echo -e "${GREEN}✅ config.js configured with: $RAILWAY_URL${NC}"
else
    echo -e "${YELLOW}⚠️  config.js configuration unclear${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "🧪 Testing signaling server..."

# Try to start the server briefly
timeout 3 node webrtc-signaling-server.js > /tmp/server-test.log 2>&1 &
SERVER_PID=$!
sleep 2

if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Signaling server starts successfully${NC}"
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
else
    echo -e "${RED}❌ Signaling server failed to start${NC}"
    echo "   Check /tmp/server-test.log for details"
    EXIT_CODE=1
fi

# Clean up
rm -f /tmp/server-test.log

echo ""
echo "📚 Checking documentation..."

DOC_FILES=(
    "NEXT-STEPS.md"
    "RAILWAY.md"
    "DEPLOYMENT-CHECKLIST.md"
    "README.md"
)

for doc in "${DOC_FILES[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✅ $doc available${NC}"
    else
        echo -e "${YELLOW}⚠️  $doc missing (not critical)${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo ""
echo "======================================"

if [ $EXIT_CODE -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Ready for Railway deployment!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Read NEXT-STEPS.md for deployment instructions"
    echo "2. Accept Railway invite: https://railway.com/invite/v4BSx3LBApG"
    echo "3. Deploy to Railway (dashboard or CLI)"
    echo "4. Update config.js with your Railway URL"
    echo "5. Deploy frontend to GitLab Pages/Vercel/Netlify"
elif [ $EXIT_CODE -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Ready with $WARNINGS warning(s)${NC}"
    echo ""
    echo "The project can be deployed, but you may want to address the warnings above."
    echo "Read NEXT-STEPS.md for deployment instructions."
else
    echo -e "${RED}❌ Not ready for deployment${NC}"
    echo ""
    echo "Please fix the errors above before deploying."
    echo ""
    echo "Common fixes:"
    echo "  - Install Node.js: https://nodejs.org/"
    echo "  - Install dependencies: npm install"
    echo "  - Check file permissions: chmod +x *.sh"
fi

echo ""

exit $EXIT_CODE
