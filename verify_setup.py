# Run verification script in TouchDesigner
import subprocess
import time
import json
import os

print("="*60)
print("RUNNING VERIFICATION IN TOUCHDESIGNER")
print("="*60)

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

$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue
if ($td) {
    [WinAPI]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
    Start-Sleep -Milliseconds 500
    
    [System.Windows.Forms.SendKeys]::SendWait("%t")
    Start-Sleep -Milliseconds 800
    
    [System.Windows.Forms.SendKeys]::SendWait("^a")
    Start-Sleep -Milliseconds 200
    
    $cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verify_to_file.py').read())"
    [System.Windows.Forms.SendKeys]::SendWait($cmd)
    Start-Sleep -Milliseconds 400
    
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 2000
}
"""

with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/verify_now.ps1', 'w') as f:
    f.write(ps_script)

subprocess.run([
    'powershell', '-ExecutionPolicy', 'Bypass',
    '-File', 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/verify_now.ps1'
], timeout=10)

print("\nWaiting for verification to complete...")
time.sleep(3)

# Read the result
result_file = 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verification_result.json'
if os.path.exists(result_file):
    with open(result_file, 'r') as f:
        result = json.load(f)
    
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    print(json.dumps(result, indent=2))
    
    if result.get('status') == 'SUCCESS':
        print("\n✅ SETUP SUCCESSFUL!")
    else:
        print("\n⚠️ SETUP INCOMPLETE")
else:
    print("\n⚠️ Verification file not found")
