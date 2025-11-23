"""
Comprehensive System Check - Switch to TouchDesigner and capture
"""
import pyautogui
import time
import subprocess

print("="*60)
print("COMPREHENSIVE TOUCHDESIGNER VERIFICATION")
print("="*60)

# Step 1: Activate TouchDesigner
print("\n[1/4] Activating TouchDesigner window...")
subprocess.run(['powershell', '-Command',
    'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
    '[Microsoft.VisualBasic.Interaction]::AppActivate("TouchDesigner")'],
    shell=True, capture_output=True)
time.sleep(2)

# Step 2: Maximize window
print("[2/4] Maximizing window...")
pyautogui.hotkey('win', 'up')
time.sleep(1)

# Step 3: Take screenshot
print("[3/4] Capturing TouchDesigner screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\touchdesigner_view.png')
print("[OK] Screenshot saved: touchdesigner_view.png")

# Step 4: Check for webrender operator (look for it)
print("\n[4/4] Looking for webrender_livekit_input operator...")
print("Screenshot captured - ready for analysis")

print("\n" + "="*60)
print("NEXT: Analyzing screenshot for video content...")
print("="*60)
