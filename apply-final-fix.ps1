Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "APPLYING FINAL COMPREHENSIVE FIX..." -ForegroundColor Cyan

$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1

if (-not $td) {
    Write-Host "ERROR: TouchDesigner not found" -ForegroundColor Red
    exit 1
}

[Native.Window]::ShowWindow($td.MainWindowHandle, 9) | Out-Null
[Native.Window]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

$cmd = "execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/final_comprehensive_fix.py')"
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 4000

Write-Host ""
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host "FINAL FIX APPLIED!" -ForegroundColor Green
Write-Host "=" -NoNewline; for($i=0;$i -lt 79;$i++){Write-Host "=" -NoNewline}; Write-Host ""
Write-Host ""
Write-Host "CHECK TOUCHDESIGNER NOW:" -ForegroundColor Yellow
Write-Host "  1. Look at WebRender TOP" -ForegroundColor White
Write-Host "  2. Should see full-screen video" -ForegroundColor White
Write-Host "  3. If not, click Reload parameter" -ForegroundColor White
Write-Host ""
Write-Host "Also opening td-input-viewer in browser for comparison..." -ForegroundColor Cyan
Start-Sleep -Milliseconds 1000

# Open the viewer page in browser for comparison
Start-Process "http://localhost:3000/td-input-viewer.html"

Write-Host ""
Write-Host "Browser opened with td-input-viewer.html" -ForegroundColor Green
Write-Host "If you see video in browser, it should work in TouchDesigner too!" -ForegroundColor Yellow
Write-Host ""
