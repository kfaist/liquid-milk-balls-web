"""
Wait for OBS to load, then start streaming
"""

import time
import subprocess
import pyautogui

print("="*60)
print("OBS STREAMING - FRESH TOKEN APPLIED")
print("="*60)

# Wait for OBS to fully load
print("\n[1/3] Waiting for OBS to load (10 seconds)...")
time.sleep(10)

# Activate OBS window
print("\n[2/3] Activating OBS window...")
try:
    subprocess.run(['powershell',
        'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
        '[Microsoft.VisualBasic.Interaction]::AppActivate("OBS")'],
        shell=True, timeout=5)
    print("[OK] OBS activated")
    time.sleep(2)
except Exception as e:
    print(f"[WARNING] {e}")

# Click Start Streaming
print("\n[3/3] Clicking 'Start Streaming' button...")

# Get screen size and estimate button location
screen_width, screen_height = pyautogui.size()
estimated_x = int(screen_width * 0.87)
estimated_y = int(screen_height * 0.75)

print(f"[INFO] Moving to: ({estimated_x}, {estimated_y})")
pyautogui.moveTo(estimated_x, estimated_y, duration=0.5)
time.sleep(0.5)

print("[ACTION] Clicking...")
pyautogui.click()
time.sleep(2)

print("\n" + "="*60)
print("[SUCCESS] Streaming should be starting now!")
print("\nCheck OBS:")
print("- Should connect without error")
print("- Button changes to 'Stop Streaming'")
print("- Streaming indicator turns green/red")
print("\nIf successful:")
print("- return-viewer.html will show video!")
print("="*60)
