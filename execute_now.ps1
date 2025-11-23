
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
    }
"@

# Find TouchDesigner
$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue
if (-not $td) {
    Write-Host "ERROR: TouchDesigner not running"
    exit 1
}

Write-Host "Found TouchDesigner (PID: $($td.Id))"

# Focus window
$hwnd = $td.MainWindowHandle
[WinAPI]::SetForegroundWindow($hwnd) | Out-Null
Start-Sleep -Milliseconds 800

# Open textport
Write-Host "Opening textport..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1200

# Clear any existing text
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 200

# Type the command
$cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_CORRECT.py').read())"
Write-Host "Sending: $cmd"
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500

# Execute
Write-Host "Executing..."
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 3000

Write-Host "Command sent!"
