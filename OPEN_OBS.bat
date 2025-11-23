@echo off
echo ============================================
echo OPENING OBS STUDIO
echo ============================================
echo.

REM Try default installation path
if exist "C:\Program Files\obs-studio\bin\64bit\obs64.exe" (
    echo [OK] Found OBS at default location
    echo [ACTION] Starting OBS...
    start "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
    timeout /t 3
    echo.
    echo [SUCCESS] OBS should be opening now
    echo.
    echo NEXT STEPS:
    echo 1. Wait for OBS to fully load
    echo 2. Click the "Start Streaming" button
    echo 3. Check return-viewer.html for video
    echo.
    echo ============================================
    pause
    exit /b 0
)

REM Try alternate installation path
if exist "C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe" (
    echo [OK] Found OBS at alternate location
    start "" "C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe"
    timeout /t 3
    exit /b 0
)

echo [ERROR] OBS not found at expected locations
echo.
echo Please check if OBS is installed at:
echo - C:\Program Files\obs-studio\bin\64bit\obs64.exe
echo - C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe
echo.
pause
