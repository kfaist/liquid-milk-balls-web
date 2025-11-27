@echo off
REM ============================================
REM  LiveKit Audio Transcription to TouchDesigner
REM ============================================
REM Captures REMOTE WEB USER's microphone from LiveKit
REM and sends transcriptions to TouchDesigner via UDP.
REM
REM P6 = Full transcript
REM P5 = Most concrete noun phrase (sticky)
REM ============================================

REM === Activate Conda environment ===
call "%USERPROFILE%\miniconda3\Scripts\activate.bat" aiart

REM === Parameters ===
set ROOM=%1
if "%ROOM%"=="" set ROOM=claymation-live
set ADDR=%2
if "%ADDR%"=="" set ADDR=127.0.0.1
set PORT=%3
if "%PORT%"=="" set PORT=8020
set MODEL=%4
if "%MODEL%"=="" set MODEL=small.en

echo.
echo ============================================
echo  LiveKit Audio Transcription
echo ============================================
echo  Room:  %ROOM%
echo  UDP:   %ADDR%:%PORT%
echo  Model: %MODEL%
echo.
echo  Listening for REMOTE WEB USERS' audio
echo  (not your local microphone)
echo ============================================
echo.

python "%~dp0transcribe_livekit_to_udp.py" --room %ROOM% --addr %ADDR% --port %PORT% --model %MODEL% --window 2.0

if errorlevel 1 (
    echo.
    echo ============================================
    echo  ERROR - Missing dependencies?
    echo ============================================
    echo  Run: pip install livekit torch openai-whisper nltk spacy soundfile numpy
    echo  Run: python -m spacy download en_core_web_sm
    echo ============================================
)
pause
