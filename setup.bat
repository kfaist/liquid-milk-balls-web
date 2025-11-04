@echo off
REM The Mirror's Echo - Setup Script for Windows
REM This script helps set up the development environment on Windows

echo.
echo 🪞 The Mirror's Echo - Setup Script (Windows)
echo ==================================================
echo.

REM Check if Node.js is installed
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed.
    echo.
    echo Please install Node.js from https://nodejs.org/
    echo.
    echo Download the Windows Installer (.msi) for your system:
    echo   - Recommended: LTS version (e.g., v20.11.0)
    echo   - 64-bit systems: Download the x64 .msi installer
    echo   - 32-bit systems: Download the x86 .msi installer
    echo.
    echo After installation:
    echo   1. Close and reopen PowerShell/Command Prompt
    echo   2. Run this setup script again: setup.bat
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version 2^>nul') do set NODE_VERSION=%%i
if not defined NODE_VERSION set NODE_VERSION=unknown
echo ✅ Node.js is installed: %NODE_VERSION%

REM Check if npm is installed
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed.
    echo.
    echo npm should be included with Node.js installation.
    echo Please reinstall Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version 2^>nul') do set NPM_VERSION=%%i
if not defined NPM_VERSION set NPM_VERSION=unknown
echo ✅ npm is installed: %NPM_VERSION%

echo.
echo 📦 Installing dependencies...
call npm install

if %errorlevel% equ 0 (
    echo.
    echo ✅ Dependencies installed successfully!
) else (
    echo.
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🎉 Setup complete!
echo.
echo To start the application:
echo   1. Start the server: npm start
echo   2. Open http://localhost:3000 in your browser
echo.
echo The server includes:
echo   • HTTP server for static files
echo   • WebSocket signaling for simple WebRTC (peer-to-peer)
echo   • LiveKit token generation (requires environment variables)
echo.
echo For detailed WebRTC setup instructions, see WEBRTC-SETUP.md
echo.
echo Happy coding! ✨
echo.
pause
