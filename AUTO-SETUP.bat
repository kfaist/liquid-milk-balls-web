@echo off
setlocal
cls
echo.
echo ============================================================
echo TOUCHDESIGNER SETUP - AUTOMATED
echo ============================================================
echo.
echo Waiting 2 seconds...
ping 127.0.0.1 -n 3 >nul

echo Sending Alt+T...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%%t')"
ping 127.0.0.1 -n 2 >nul

echo Clearing textport...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^a')"
ping 127.0.0.1 -n 1 >nul

echo Typing command...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('exec(open(''C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py'').read())')"
ping 127.0.0.1 -n 1 >nul

echo Executing...
powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')"
ping 127.0.0.1 -n 3 >nul

echo.
echo ============================================================
echo DONE! Check TouchDesigner textport for output.
echo ============================================================
