Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "=" -NoNewline
for($i=0; $i -lt 79; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host "AUTOMATING TOUCHDESIGNER SETUP"
Write-Host "=" -NoNewline
for($i=0; $i -lt 79; $i++) { Write-Host "=" -NoNewline }
Write-Host ""

# Find TouchDesigner
Write-Host ""
Write-Host "Finding TouchDesigner window..."
$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1

if (-not $td) {
    Write-Host "ERROR: No TouchDesigner window found!" -ForegroundColor Red
    exit 1
}

Write-Host "FOUND: $($td.MainWindowTitle)" -ForegroundColor Green
Write-Host "PID: $($td.Id)"

# Bring to foreground
Write-Host ""
Write-Host "Bringing TouchDesigner to foreground..."
[Native.Window]::ShowWindow($td.MainWindowHandle, 9) | Out-Null
[Native.Window]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500
Write-Host "TouchDesigner is now active" -ForegroundColor Green

# Send Alt+T
Write-Host ""
Write-Host "Opening textport (Alt+T)..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Type command
$cmd = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/ultimate_td_setup.py')"
Write-Host "Typing command..."
Write-Host "  $cmd" -ForegroundColor Yellow
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500

# Send Enter
Write-Host "Pressing Enter..."
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 2000

Write-Host ""
Write-Host "=" -NoNewline
for($i=0; $i -lt 79; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host "SETUP COMMAND EXECUTED!" -ForegroundColor Green
Write-Host "=" -NoNewline
for($i=0; $i -lt 79; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host ""
Write-Host "CHECK TOUCHDESIGNER NOW:"
Write-Host "  1. Look at the textport output"
Write-Host "  2. Find the Web Client TOP"
Write-Host "  3. YOU SHOULD SEE VIDEO!" -ForegroundColor Green
Write-Host ""
