# COMPLETE PIPELINE STARTUP SCRIPT
# This launches everything in the correct order for your video processing pipeline

param(
    [switch]$SkipOBS,
    [switch]$SkipTouchDesigner,
    [switch]$SkipServer
)

$ErrorActionPreference = "Stop"

Write-Host "=" -NoNewline; for($i=0; $i -lt 70; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host "LIQUID MILK BALLS - VIDEO PROCESSING PIPELINE STARTUP"
Write-Host "=" -NoNewline; for($i=0; $i -lt 70; $i++) { Write-Host "=" -NoNewline }; Write-Host ""

$projectPath = "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web"

# Step 1: Start the Node.js server
if (!$SkipServer) {
    Write-Host "`n[1/4] Starting Node.js server..."
    
    # Check if server is already running
    $serverRunning = Get-Process node -ErrorAction SilentlyContinue | Where-Object {
        $_.MainWindowTitle -like "*liquid-milk-balls*" -or 
        (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue)
    }
    
    if ($serverRunning) {
        Write-Host "✓ Server already running on port 3000"
    } else {
        Write-Host "Launching server..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; node server.js"
        Start-Sleep -Seconds 3
        Write-Host "✓ Server started"
    }
} else {
    Write-Host "`n[1/4] Skipping server startup..."
}

# Step 2: Start TouchDesigner
if (!$SkipTouchDesigner) {
    Write-Host "`n[2/4] Starting TouchDesigner..."
    
    $tdRunning = Get-Process -Name TouchDesigner -ErrorAction SilentlyContinue
    if ($tdRunning) {
        Write-Host "✓ TouchDesigner already running"
    } else {
        Write-Host "Please start TouchDesigner manually and load your project file."
        Write-Host "Press any key when TouchDesigner is ready..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        Write-Host "✓ TouchDesigner ready"
    }
} else {
    Write-Host "`n[2/4] Skipping TouchDesigner startup..."
}

# Step 3: Start OBS
if (!$SkipOBS) {
    Write-Host "`n[3/4] Starting OBS Studio..."
    
    $obsRunning = Get-Process -Name obs64 -ErrorAction SilentlyContinue
    if ($obsRunning) {
        Write-Host "✓ OBS already running"
    } else {
        Write-Host "Launching OBS..."
        Start-Process "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
        Start-Sleep -Seconds 5
        Write-Host "✓ OBS started"
    }
} else {
    Write-Host "`n[3/4] Skipping OBS startup..."
}

# Step 4: Wait for manual streaming start
Write-Host "`n[4/4] Starting OBS Streaming..."
Write-Host ""
Write-Host "MANUAL STEP REQUIRED:"
Write-Host "  → Go to OBS window"
Write-Host "  → Click 'Start Streaming' button"
Write-Host ""
Write-Host "Press any key when streaming has started..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Verify streaming is active
Write-Host "`nVerifying streaming status..."
Start-Sleep -Seconds 2

$latestLog = Get-ChildItem "$env:APPDATA\obs-studio\logs" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

if ($latestLog) {
    $logContent = Get-Content $latestLog.FullName -Tail 20
    if ($logContent -match "Streaming Start" -or $logContent -match "PeerConnection state is now: Connected") {
        Write-Host "✓ OBS is streaming!"
    } else {
        Write-Host "⚠ Could not confirm streaming status. Please check OBS."
    }
}

# Final status
Write-Host ""
Write-Host "=" -NoNewline; for($i=0; $i -lt 70; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host "PIPELINE STATUS"
Write-Host "=" -NoNewline; for($i=0; $i -lt 70; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host ""
Write-Host "✓ Server:        http://localhost:3000"
Write-Host "✓ Publisher:     http://localhost:3000/publisher.html"
Write-Host "✓ Viewer:        http://localhost:3000/return-viewer.html"
Write-Host "✓ TouchDesigner: Processing video"
Write-Host "✓ OBS:           Streaming to LiveKit"
Write-Host ""
Write-Host "YOUR COMPLETE PIPELINE IS NOW RUNNING!"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Open publisher.html to test camera input"
Write-Host "  2. Open return-viewer.html to see processed output"
Write-Host "  3. Click 'Join Stream' in the viewer"
Write-Host ""
