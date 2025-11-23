Add-Type -AssemblyName System.Windows.Forms

# Wait for OBS to be ready
Start-Sleep -Seconds 2

# Find and activate OBS window
$processes = Get-Process | Where-Object {$_.ProcessName -like "*obs*"}
if ($processes) {
    $obsProcess = $processes[0]
    Write-Host "Found OBS process: $($obsProcess.ProcessName)"
    
    # Bring OBS to foreground
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class WinAPI {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        }
"@
    
    $handle = $obsProcess.MainWindowHandle
    if ($handle -ne [IntPtr]::Zero) {
        [WinAPI]::ShowWindow($handle, 5) # SW_SHOW
        [WinAPI]::SetForegroundWindow($handle)
        Write-Host "OBS window activated"
        
        Start-Sleep -Milliseconds 1000
        
        # Try to use Controls panel hotkey
        # By default, Start/Stop Streaming might not have a hotkey
        # So we'll try to navigate to the button
        
        # Check if already streaming by trying to access OBS logs
        Write-Host "Attempting to start streaming..."
        Write-Host "Please click 'Start Streaming' button in OBS manually"
        Write-Host "Or set up a hotkey in OBS: Settings > Hotkeys > Start Streaming"
        
    } else {
        Write-Host "Could not get OBS window handle"
    }
} else {
    Write-Host "OBS not found"
}
