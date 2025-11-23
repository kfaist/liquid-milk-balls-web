# AUTO-EXECUTE TOUCHDESIGNER SETUP
# This script will send keystrokes to TouchDesigner to run our setup

Add-Type -AssemblyName System.Windows.Forms

Write-Host "🎯 AUTOMATING TOUCHDESIGNER SETUP" -ForegroundColor Cyan
Write-Host ("=" * 80)

# Find TouchDesigner window
Write-Host "`n📍 Finding TouchDesigner window..."
$tdProcesses = Get-Process | Where-Object {$_.ProcessName -eq "TouchDesigner" -and $_.MainWindowTitle -ne ""}

if ($tdProcesses.Count -eq 0) {
    Write-Host "❌ No TouchDesigner windows found!" -ForegroundColor Red
    exit 1
}

# Use the first TouchDesigner window
$tdProcess = $tdProcesses[0]
Write-Host "✅ Found TouchDesigner: $($tdProcess.MainWindowTitle)" -ForegroundColor Green
Write-Host "   PID: $($tdProcess.Id)"

# Bring TouchDesigner to foreground
Write-Host "`n🔄 Bringing TouchDesigner to foreground..."
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WindowHelper {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$handle = $tdProcess.MainWindowHandle
[WindowHelper]::ShowWindow($handle, 9) # SW_RESTORE
[WindowHelper]::SetForegroundWindow($handle)
Start-Sleep -Milliseconds 500

Write-Host "✅ TouchDesigner is now in foreground" -ForegroundColor Green

# Send Alt+T to open textport
Write-Host "`n⌨️  Sending Alt+T to open textport..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Type the command
$command = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/ultimate_td_setup.py')"
Write-Host "⌨️  Typing command..."
Write-Host "   $command" -ForegroundColor Yellow

[System.Windows.Forms.SendKeys]::SendWait($command)
Start-Sleep -Milliseconds 500

# Send Enter
Write-Host "⌨️  Pressing Enter..."
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 1000

Write-Host "`n" + ("=" * 80)
Write-Host "✅ COMMAND SENT TO TOUCHDESIGNER!" -ForegroundColor Green
Write-Host ("=" * 80)
Write-Host "`n📋 What happened:"
Write-Host "   1. ✅ Found TouchDesigner window"
Write-Host "   2. ✅ Brought it to foreground"
Write-Host "   3. ✅ Opened textport (Alt+T)"
Write-Host "   4. ✅ Typed setup command"
Write-Host "   5. ✅ Pressed Enter"
Write-Host "`n👀 CHECK TOUCHDESIGNER NOW!"
Write-Host "   - Look at the textport output"
Write-Host "   - Find the Web Client TOP"
Write-Host "   - YOU SHOULD SEE VIDEO!" -ForegroundColor Green
Write-Host "`n" + ("=" * 80)
