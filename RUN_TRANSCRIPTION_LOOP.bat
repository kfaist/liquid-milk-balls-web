@echo off
REM ============================================
REM The Mirror's Echo - Transcription Loop
REM ============================================
REM This script automatically restarts the transcription
REM after each session ends, ensuring fresh memory
REM and avoiding memory leaks from Whisper/spaCy.
REM
REM Press Ctrl+C to stop the loop.
REM ============================================

echo.
echo ========================================
echo  The Mirror's Echo - Transcription Loop
echo ========================================
echo.
echo This will automatically restart transcription
echo after each user session ends.
echo.
echo Press Ctrl+C to stop.
echo.

:loop
echo.
echo ----------------------------------------
echo [%date% %time%] Starting new transcription instance...
echo ----------------------------------------
echo.

python transcribe_livekit_to_udp.py --room claymation-live --port 8020

echo.
echo [%date% %time%] Transcription ended. Waiting 3 seconds before restart...
timeout /t 3 /nobreak > nul

goto loop
