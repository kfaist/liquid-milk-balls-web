# Automated TouchDesigner Setup Execution
import subprocess
import time

print("="*60)
print("TOUCHDESIGNER SETUP - AUTOMATED EXECUTION")
print("="*60)

# Method 1: Try using PowerShell SendKeys
print("\nAttempting automated execution via PowerShell...")

ps_script = """
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
    }
"@

# Find TouchDesigner
$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue
if (-not $td) {
    Write-Host "ERROR: TouchDesigner not running"
    exit 1
}

Write-Host "Found TouchDesigner (PID: $($td.Id))"

# Focus window
$hwnd = $td.MainWindowHandle
[WinAPI]::SetForegroundWindow($hwnd) | Out-Null
Start-Sleep -Milliseconds 800

# Open textport
Write-Host "Opening textport..."
[System.Windows.Forms.SendKeys]::SendWait("%t")
Start-Sleep -Milliseconds 1200

# Clear any existing text
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 200

# Type the command
$cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_CORRECT.py').read())"
Write-Host "Sending: $cmd"
[System.Windows.Forms.SendKeys]::SendWait($cmd)
Start-Sleep -Milliseconds 500

# Execute
Write-Host "Executing..."
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Milliseconds 3000

Write-Host "Command sent!"
"""

# Write and execute the PowerShell script
with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/execute_now.ps1', 'w') as f:
    f.write(ps_script)

result = subprocess.run([
    'powershell', 
    '-ExecutionPolicy', 'Bypass',
    '-File', 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/execute_now.ps1'
], capture_output=True, text=True, timeout=15)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n" + "="*60)
print("EXECUTION COMPLETE")
print("="*60)
print("\nWaiting 3 seconds for TouchDesigner to process...")
time.sleep(3)

print("\nChecking verification file...")
