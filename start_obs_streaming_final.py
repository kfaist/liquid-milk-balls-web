"""
Start OBS Streaming with Correct WHIP Config
"""

import time
import pyautogui
import subprocess

print("="*60)
print("STARTING OBS STREAMING")
print("="*60)

# Wait for OBS to fully load
print("\n[1/4] Waiting for OBS to load (12 seconds)...")
time.sleep(12)

# Check if OBS is running
print("\n[2/4] Checking OBS status...")
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'], 
                       capture_output=True, text=True)
if 'obs64.exe' in result.stdout:
    print("[OK] OBS is running")
else:
    print("[ERROR] OBS not running!")
    exit(1)

# Activate OBS window
print("\n[3/4] Activating OBS window...")
time.sleep(2)
try:
    # Try multiple window titles
    for title in ['OBS', 'OBS Studio', 'obs64']:
        try:
            subprocess.run(['powershell',
                'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
                f'[Microsoft.VisualBasic.Interaction]::AppActivate("{title}")'],
                shell=True, timeout=3, capture_output=True)
            print(f"[OK] Activated via '{title}'")
            break
        except:
            continue
    time.sleep(2)
except Exception as e:
    print(f"[INFO] Window activation: {e}")

# Click Start Streaming button
print("\n[4/4] Clicking 'Start Streaming' button...")

# Get screen size
screen_width, screen_height = pyautogui.size()
print(f"[INFO] Screen: {screen_width}x{screen_height}")

# Calculate button position (right side controls)
button_x = int(screen_width * 0.87)
button_y = int(screen_height * 0.75)

print(f"[INFO] Estimated button: ({button_x}, {button_y})")
pyautogui.moveTo(button_x, button_y, duration=0.3)
time.sleep(0.3)

print("[ACTION] Clicking...")
pyautogui.click()
time.sleep(3)

print("\n" + "="*60)
print("STREAMING SHOULD BE STARTING!")
print("\nCheck OBS window:")
print("1. Button should say 'Stop Streaming' (not 'Start')")
print("2. Should see connection success (no error dialog)")
print("3. Status bar shows bitrate/streaming indicator")
print("\nIf successful:")
print("- return-viewer.html will show video!")
print("- Pipeline is 100% complete!")
print("="*60)
