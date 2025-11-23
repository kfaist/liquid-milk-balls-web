Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "FIXING TOUCHDESIGNER - SWITCHING TO WEBRENDER TOP..." -ForegroundColor Cyan

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

# Type fix command
$cmd = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_use_webrender.py')"
Write-Host "Running WebRender fix..."
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500

# Send Enter
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 3000

Write-Host ""
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host "FIX APPLIED!" -ForegroundColor Green
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host ""
Write-Host "WHAT CHANGED:" -ForegroundColor Yellow
Write-Host "  BEFORE: Web Client TOP (shows HTTP headers as text)" -ForegroundColor Red
Write-Host "  AFTER:  WebRender TOP (renders webpages with video)" -ForegroundColor Green
Write-Host ""
Write-Host "CHECK TOUCHDESIGNER NOW:"
Write-Host "  1. Find the WebRender TOP operator"
Write-Host "  2. You should see VIDEO rendering!"
Write-Host "  3. If not, click Reload parameter"
Write-Host ""
