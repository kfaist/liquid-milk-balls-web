Add-Type -AssemblyName System.Windows.Forms
Add-Type -Name Window -Namespace Native -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

Write-Host "CHECKING TOUCHDESIGNER CONFIGURATION..." -ForegroundColor Cyan

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
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1000

# Check current configuration
$cmd = @"
print('='*80)
print('CHECKING CURRENT TOUCHDESIGNER CONFIGURATION')
print('='*80)

# Check for WebRender TOPs
webrender_tops = root.findChildren(type='webrenderTOP')
print(f'\nWebRender TOPs found: {len(webrender_tops)}')
for i, wr in enumerate(webrender_tops, 1):
    print(f'\n  WebRender TOP #{i}:')
    print(f'    Name: {wr.name}')
    print(f'    Path: {wr.path}')
    try:
        url = wr.par.url.eval()
        print(f'    URL: {url}')
        print(f'    Active: {wr.par.active.eval()}')
        print(f'    Resolution: {wr.par.resolutionw.eval()} x {wr.par.resolutionh.eval()}')
        if 'td-input-viewer' in url:
            print(f'    STATUS: CORRECT URL!')
        elif 'publisher' in url:
            print(f'    STATUS: WRONG URL - needs td-input-viewer.html')
        else:
            print(f'    STATUS: Unknown URL')
    except Exception as e:
        print(f'    ERROR: {e}')

# Check for Web Client TOPs
webclient_tops = root.findChildren(type='webclientTOP')
print(f'\n\nWeb Client TOPs found: {len(webclient_tops)}')
for i, wc in enumerate(webclient_tops, 1):
    print(f'\n  Web Client TOP #{i}:')
    print(f'    Name: {wc.name}')
    print(f'    Path: {wc.path}')
    try:
        url = wc.par.url.eval()
        print(f'    URL: {url}')
        print(f'    NOTE: Web Client TOPs show HTTP headers, not webpages!')
    except:
        pass

print('\n' + '='*80)
"@

[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 3000

Write-Host ""
Write-Host "CHECK TOUCHDESIGNER TEXTPORT FOR CONFIGURATION DETAILS" -ForegroundColor Green
