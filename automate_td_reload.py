"""
TouchDesigner Automation - Uses Windows automation to reload webrender
"""

import pyautogui
import time
import subprocess

print("="*60)
print("TOUCHDESIGNER WEBRENDER AUTOMATION")
print("="*60)

# Step 1: Find TouchDesigner window
print("\n[1/4] Finding TouchDesigner window...")
result = subprocess.run(['powershell', 
    '(Get-Process | Where-Object {$_.ProcessName -like "*TouchDesigner*"}).MainWindowTitle'],
    capture_output=True, text=True)

if result.stdout.strip():
    print(f"[OK] Found TouchDesigner: {result.stdout.strip()}")
else:
    print("[ERROR] TouchDesigner window not found")
    print("Make sure TouchDesigner is running and not minimized")
    exit(1)

# Step 2: Activate TouchDesigner window
print("\n[2/4] Activating TouchDesigner window...")
subprocess.run(['powershell',
    'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
    '[Microsoft.VisualBasic.Interaction]::AppActivate("TouchDesigner")'],
    shell=True)
time.sleep(1)

# Step 3: Open Textport (Alt+T)
print("\n[3/4] Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(1)

# Step 4: Type reload command
print("\n[4/4] Sending reload command...")
command = "op('/webrender_livekit_input').par.reload.pulse()"
pyautogui.typewrite(command, interval=0.05)
time.sleep(0.5)
pyautogui.press('enter')

print("\n[SUCCESS] Reload command sent to TouchDesigner!")
print("Check the webrender_livekit_input operator for video")
print("="*60)
