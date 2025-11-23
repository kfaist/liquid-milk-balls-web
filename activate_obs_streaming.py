"""
Activate OBS and Start Streaming
Uses Windows automation to click the Start Streaming button
"""

import pyautogui
import time
import subprocess

print("="*60)
print("OBS STREAMING ACTIVATION")
print("="*60)

# Step 1: Activate OBS window
print("\n[1/3] Activating OBS Studio...")
try:
    subprocess.run(['powershell',
        'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
        '[Microsoft.VisualBasic.Interaction]::AppActivate("OBS")'],
        shell=True, timeout=5)
    print("[OK] OBS window activated")
    time.sleep(2)
except Exception as e:
    print(f"[WARNING] Could not activate OBS: {e}")

# Step 2: Look for "Start Streaming" button
print("\n[2/3] Locating 'Start Streaming' button...")
print("[INFO] Looking for button on screen...")

try:
    # Try to find the button
    # OBS typically has this in the controls panel on the right
    button_location = pyautogui.locateOnScreen('start_streaming_button.png', confidence=0.7)
    if button_location:
        print(f"[OK] Found button at {button_location}")
        pyautogui.click(button_location)
        print("[SUCCESS] Clicked 'Start Streaming' button!")
    else:
        print("[INFO] Button image not found, trying text-based approach...")
        raise Exception("Image not found")
except:
    # Fallback: Look for typical button location
    # OBS "Start Streaming" is usually in the bottom right controls area
    print("[INFO] Using estimated button location...")
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Typical OBS layout: Controls on right side
    # "Start Streaming" button is usually around 85-90% across, 70-80% down
    estimated_x = int(screen_width * 0.87)
    estimated_y = int(screen_height * 0.75)
    
    print(f"[INFO] Screen size: {screen_width}x{screen_height}")
    print(f"[INFO] Estimated button location: ({estimated_x}, {estimated_y})")
    print("[ACTION] Moving mouse to estimated location...")
    
    pyautogui.moveTo(estimated_x, estimated_y, duration=0.5)
    time.sleep(0.5)
    
    print("[ACTION] Clicking...")
    pyautogui.click()
    time.sleep(1)

# Step 3: Verify
print("\n[3/3] Verifying stream started...")
print("[INFO] Check OBS - should show 'Stop Streaming' button now")
print("[INFO] Check bottom status bar for streaming indicator")
print("\n" + "="*60)
print("If streaming started successfully:")
print("- OBS shows 'Stop Streaming' button")
print("- Green/red dot indicator shows streaming")
print("- return-viewer.html should now show video!")
print("="*60)
