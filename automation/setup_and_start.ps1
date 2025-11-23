# OBS Hotkey Setup and Auto-Start Script
# This script adds a hotkey for "Start Streaming" in OBS config
# Then uses that hotkey to automate streaming

$ErrorActionPreference = "Stop"

# OBS global config path
$obsGlobalConfig = "$env:APPDATA\obs-studio\global.ini"

Write-Host "=" -NoNewline; for($i=0; $i -lt 60; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host "OBS Auto-Start Streaming Setup"
Write-Host "=" -NoNewline; for($i=0; $i -lt 60; $i++) { Write-Host "=" -NoNewline }; Write-Host ""

# Function to add hotkey to OBS config
function Set-OBSStreamingHotkey {
    Write-Host "`nConfiguring OBS hotkey for Start Streaming..."
    
    if (!(Test-Path $obsGlobalConfig)) {
        Write-Host "Error: OBS config not found at $obsGlobalConfig"
        return $false
    }
    
    # Read current config
    $config = Get-Content $obsGlobalConfig
    
    # Check if Hotkeys section exists
    $hotkeySection = $config | Select-String -Pattern "\[Hotkeys\]"
    
    if (!$hotkeySection) {
        # Add Hotkeys section
        Add-Content -Path $obsGlobalConfig -Value "`n[Hotkeys]"
        Add-Content -Path $obsGlobalConfig -Value "OBSBasic.StartStreaming=`"{\`"OBSBasic.StartStreaming\`": [ {\`"key\`": \`"OBS_KEY_F9\`" } ]}`""
        Write-Host "✓ Added F9 hotkey for Start Streaming"
    } else {
        Write-Host "✓ Hotkeys section already exists"
        # Check if StartStreaming hotkey exists
        $streamingHotkey = $config | Select-String -Pattern "OBSBasic.StartStreaming"
        if (!$streamingHotkey) {
            # Find the [Hotkeys] line and add the hotkey after it
            $newConfig = @()
            foreach ($line in $config) {
                $newConfig += $line
                if ($line -match "\[Hotkeys\]") {
                    $newConfig += "OBSBasic.StartStreaming=`"{\`"OBSBasic.StartStreaming\`": [ {\`"key\`": \`"OBS_KEY_F9\`" } ]}`""
                }
            }
            $newConfig | Set-Content $obsGlobalConfig
            Write-Host "✓ Added F9 hotkey for Start Streaming"
        } else {
            Write-Host "✓ Start Streaming hotkey already configured"
        }
    }
    
    return $true
}

# Function to check if OBS is running
function Test-OBSRunning {
    $obs = Get-Process -Name obs64 -ErrorAction SilentlyContinue
    return ($null -ne $obs)
}

# Main script
Write-Host "`n1. Setting up OBS hotkey..."
Set-OBSStreamingHotkey

Write-Host "`n2. Checking if OBS is running..."
if (!(Test-OBSRunning)) {
    Write-Host "Launching OBS..."
    Start-Process "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
    
    Write-Host "Waiting for OBS to start..."
    $timeout = 0
    while (!(Test-OBSRunning) -and $timeout -lt 30) {
        Start-Sleep -Seconds 1
        $timeout++
    }
    
    if (Test-OBSRunning) {
        Write-Host "✓ OBS started successfully"
    } else {
        Write-Host "✗ OBS failed to start"
        exit 1
    }
} else {
    Write-Host "✓ OBS is already running"
}

Write-Host "`n3. Waiting for OBS to fully load..."
Start-Sleep -Seconds 4

Write-Host "`n4. Sending F9 hotkey to start streaming..."

# Install VirtualDesktop.AutomationHelper if not available
if (!(Get-Module -ListAvailable -Name VirtualDesktop.AutomationHelper)) {
    Write-Host "Installing automation helper..."
