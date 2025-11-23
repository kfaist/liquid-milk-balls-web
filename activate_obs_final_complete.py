"""
FINAL OBS STREAMING ACTIVATION - Complete Solution
Waits for OBS, activates window, clicks Start Streaming
"""

import time
import pyautogui
import subprocess
import sys

print("="*70)
print(" FINAL OBS STREAMING ACTIVATION - CORRECTED WHIP CONFIG")
print("="*70)

# Step 1: Wait for OBS to fully start
print("\n[STEP 1/5] Waiting for OBS to start (15 seconds)...")
for i in range(15):
    time.sleep(1)
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'], 
                           capture_output=True, text=True)
    if 'obs64.exe' in result.stdout:
        print(f"[OK] OBS detected after {i+1} seconds")
        break
    if i == 14:
        print("[ERROR] OBS not running after 15 seconds")
        print("[ACTION] Please manually open OBS Studio")
        sys.exit(1)

# Extra wait for UI to load
print("[INFO] Waiting for OBS UI to fully load...")
time.sleep(5)

# Step 2: Activate OBS window - try multiple methods
print("\n[STEP 2/5] Activating OBS window...")
activated = False

# Method 1: Try common window titles
for title in ['OBS', 'OBS Studio', 'obs64.exe']:
    try:
        result = subprocess.run([
            'powershell', '-Command',
            f"Add-Type -AssemblyName Microsoft.VisualBasic; " +
            f"[Microsoft.VisualBasic.Interaction]::AppActivate('{title}')"
        ], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print(f"[OK] Activated OBS via '{title}'")
            activated = True
            break
    except:
        continue

if not activated:
    print("[INFO] Trying alternate activation method...")
    # Method 2: Click on OBS window area
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.click(center_x, center_y)
    print(f"[INFO] Clicked center screen ({center_x}, {center_y})")

time.sleep(2)

# Step 3: Locate Start Streaming button
print("\n[STEP 3/5] Locating 'Start Streaming' button...")

screen_width, screen_height = pyautogui.size()
print(f"[INFO] Screen resolution: {screen_width}x{screen_height}")

# OBS controls are typically on right side
# "Start Streaming" button is usually around 85-90% across, 70-80% down
button_x = int(screen_width * 0.87)
button_y = int(screen_height * 0.75)

print(f"[INFO] Estimated button position: ({button_x}, {button_y})")

# Step 4: Move mouse to button
print("\n[STEP 4/5] Moving to button...")
pyautogui.moveTo(button_x, button_y, duration=0.5)
time.sleep(0.5)

# Step 5: Click Start Streaming
print("\n[STEP 5/5] Clicking 'Start Streaming'...")
pyautogui.click()
time.sleep(3)

# Verification
print("\n" + "="*70)
print(" STREAMING ACTIVATION COMPLETE!")
print("="*70)
print("\n✅ CHECK THESE NOW:")
print("\n1. OBS Window:")
print("   - Button should say 'Stop Streaming' (not 'Start')")
print("   - NO error dialog about connection failure")
print("   - Status bar shows bitrate (e.g., '3146 kbps')")
print("   - Green/red streaming indicator active")
print("\n2. Return Viewer:")
print("   - Open: http://localhost:3000/return-viewer.html")
print("   - Should show video from OBS")
print("\n" + "="*70)
print(" KEY FIX APPLIED:")
print("   Old: https://...livekit.cloud/whip?access_token=...")
print("   New: https://...whip.livekit.cloud/w + bearer token")
print("="*70)
print("\nIf streaming works = PIPELINE 100% COMPLETE! 🎉")
print("="*70)
