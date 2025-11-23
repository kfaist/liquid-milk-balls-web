@echo off
title TouchDesigner Setup - Final Execute
cls
echo.
echo ===========================================================
echo TOUCHDESIGNER WEBRTC SETUP - FINAL
echo ===========================================================
echo.
echo This will execute the setup script in TouchDesigner
echo.
echo MAKE SURE TOUCHDESIGNER IS THE ACTIVE WINDOW!
echo.
pause
echo.
echo Executing in 3 seconds...
timeout /t 1 >nul
echo Executing in 2 seconds...
timeout /t 1 >nul
echo Executing in 1 second...
timeout /t 1 >nul
echo.
echo Sending Alt+T to open textport...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%%t')"
timeout /t 1 >nul
echo.
echo Clearing textport...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^a')"
timeout /t 0.2 >nul
echo.
echo Typing command...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('exec(open(''C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py'').read())')"
timeout /t 0.5 >nul
echo.
echo Executing...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')"
timeout /t 2 >nul
echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Check TouchDesigner textport for results!
echo.
pause
