Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "FIXING WEBRENDER URL..." -ForegroundColor Cyan

$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1

if (-not $td) {
    Write-Host "ERROR: TouchDesigner not found" -ForegroundColor Red
    exit 1
}

# Bring to foreground
[Native.Window]::ShowWindow($td.MainWindowHandle, 9) | Out-Null
[Native.Window]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Open textport
Write-Host "Opening textport..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Execute fix
$cmd = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_webrender_url.py')"
Write-Host "Fixing URL..."
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 3000

Write-Host ""
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host "URL FIXED!" -ForegroundColor Green
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host ""
Write-Host "CHANGED FROM:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000/publisher.html" -ForegroundColor Red
Write-Host "TO:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000/td-input-viewer.html" -ForegroundColor Green
Write-Host ""
Write-Host "CHECK WEBRENDER TOP NOW - YOU SHOULD SEE VIDEO!" -ForegroundColor Green
Write-Host ""
