Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "VERIFYING TOUCHDESIGNER SETUP..." -ForegroundColor Cyan

# Find TouchDesigner
$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1

if (-not $td) {
    Write-Host "ERROR: TouchDesigner not found" -ForegroundColor Red
    exit 1
}

# Bring to foreground
[Native.Window]::ShowWindow($td.MainWindowHandle, 9) | Out-Null
[Native.Window]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Send Alt+T to open textport
Write-Host "Opening textport..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Type verification command
$cmd = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/verify_td_setup.py')"
Write-Host "Running verification..."
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500

# Send Enter
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 2000

Write-Host "VERIFICATION COMMAND SENT!" -ForegroundColor Green
Write-Host "Check TouchDesigner textport for results"
