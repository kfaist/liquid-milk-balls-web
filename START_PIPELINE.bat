@echo off
REM Video Processing Pipeline Startup
REM This script launches the complete pipeline automatically

echo.
echo ===============================================
echo   VIDEO PROCESSING PIPELINE STARTUP
echo ===============================================
echo.

cd /d "%~dp0"
python start_pipeline.py

pause
