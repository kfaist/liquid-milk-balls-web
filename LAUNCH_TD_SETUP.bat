@echo off
cls
echo ========================================================================
echo         LIQUID MILK BALLS - TOUCHDESIGNER CONFIGURATION
echo ========================================================================
echo.
echo This will help you connect the publisher to TouchDesigner!
echo.
echo Opening all necessary files and pages...
echo.
pause

REM Open configuration files
echo Opening configuration documentation...
start notepad "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\QUICK_START.txt"
timeout /t 1 /nobreak >nul

REM Open JSON config
echo Opening LiveKit config file...
start notepad "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\livekit_config.json"
timeout /t 1 /nobreak >nul

echo.
echo ========================================================================
echo TOUCHDESIGNER CONFIGURATION
echo ========================================================================
echo.
echo IN TOUCHDESIGNER:
echo 1. Open the Textport (Alt+T or click Textport button)
echo 2. Copy and paste this EXACT command:
echo.
echo    exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())
echo.
echo 3. Press ENTER
echo 4. The script will automatically configure LiveKit!
echo.
echo ========================================================================
echo ALTERNATIVE: MANUAL CONFIGURATION
echo ========================================================================
echo.
echo If the script doesn't work:
echo 1. In TD, create a Web Render TOP (TAB key, type "web render")
echo 2. Set these parameters (from livekit_config.json):
echo    - URL: wss://claymation-transcription-l6e51sws.livekit.cloud
echo    - Room: claymation-live
echo    - Token: eyJhbGciOiJIUzI1NiJ9... (see config file)
echo 3. Enable LiveKit mode
echo 4. Click Connect
echo.
echo ========================================================================
echo.
pause

echo.
echo Opening browser pages for testing...
echo.

REM Open publisher page
start firefox "https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html"
timeout /t 2 /nobreak >nul

REM Open test viewer
start firefox "https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-auto-viewer.html"

echo.
echo ========================================================================
echo ALL SET!
echo ========================================================================
echo.
echo What's open:
echo   - Configuration documentation
echo   - LiveKit config file
echo   - Publisher page (Firefox)
echo   - Test viewer page (Firefox)
echo.
echo Next steps:
echo   1. Configure TouchDesigner using the textport command above
echo   2. Test publisher page (click "Start Publishing")
echo   3. Video should appear in TD!
echo.
echo ========================================================================
echo.
pause
