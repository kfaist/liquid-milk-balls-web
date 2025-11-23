# Execute TouchDesigner script via keyboard automation
Add-Type -AssemblyName System.Windows.Forms

# Find TouchDesigner window
$touchdesignerProcess = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue
if (-not $touchdesignerProcess) {
    Write-Host "ERROR: TouchDesigner is not running"
    exit 1
}

Write-Host "Found TouchDesigner process (PID: $($touchdesignerProcess.Id))"

# Get the window
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();
    }
"@

$hwnd = $touchdesignerProcess.MainWindowHandle
Write-Host "Bringing TouchDesigner to foreground..."
[WinAPI]::SetForegroundWindow($hwnd)
Start-Sleep -Milliseconds 500

# Send Alt+T to open textport
Write-Host "Opening textport (Alt+T)..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Type the command
$command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_CORRECT.py').read())"
Write-Host "Sending command: $command"
[System.Windows.Forms.SendKeys]::SendWait($command)
Start-Sleep -Milliseconds 500

# Send Enter
Write-Host "Executing..."
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 2000

Write-Host ""
Write-Host "Script execution command sent!"
Write-Host "Please check TouchDesigner textport for output."
Write-Host ""
Write-Host "Expected output:"
Write-Host "  - Creating Web Render TOP"
Write-Host "  - Created: /webrender_livekit_input"
Write-Host "  - Setting up NDI Out"
Write-Host "  - Connected operators"
Write-Host "  - SETUP COMPLETE!"
