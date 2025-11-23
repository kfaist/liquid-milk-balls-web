@echo off
echo ========================================
echo TouchDesigner WebRTC Test Launcher
echo ========================================
echo.
echo Your IP Address: 192.168.24.70
echo.
echo Opening test pages in your browser...
echo.

REM Open publisher page for testing
start http://192.168.24.70:3000/publisher.html

timeout /t 2 /nobreak >nul

REM Open control center
start http://localhost:3000/control-center.html

echo.
echo ========================================
echo Pages opened!
echo ========================================
echo.
echo PUBLISHER PAGE: http://192.168.24.70:3000/publisher.html
echo   - Click "Start Publishing"
echo   - Grant camera permissions
echo   - You should see yourself
echo.
echo CONTROL CENTER: http://localhost:3000/control-center.html
echo   - Dashboard with all your pages
echo.
echo ========================================
echo Next: Set up TouchDesigner
echo ========================================
echo.
echo In TouchDesigner (ndi-streamCOPY.toe):
echo.
echo 1. Press Alt+T to open Textport
echo 2. Copy and paste this command:
echo.
echo exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_auto_setup.py').read())
echo.
echo 3. Press Enter
echo.
echo The script will automatically create:
echo   - Web Render TOP (receives WebRTC)
echo   - NDI Out TOP (sends to OBS)
echo   - Connection between them
echo.
echo ========================================
echo.
pause
