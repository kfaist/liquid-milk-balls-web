@echo off
title Mirror's Echo Transcription Service
color 0A

echo ========================================
echo   Mirror's Echo - Transcription Loop
echo   Auto-restarts on disconnect
echo ========================================
echo.

cd /d "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web"

:loop
echo [%date% %time%] Starting transcription...
python transcribe_livekit_to_udp.py --room claymation-live --port 8020

echo.
echo [%date% %time%] Transcription stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto loop
