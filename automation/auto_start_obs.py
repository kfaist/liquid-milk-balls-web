"""
OBS Auto-Start Streaming Script
This script launches OBS and automatically clicks "Start Streaming"
Uses pyautogui for GUI automation
"""

import time
import subprocess
import pyautogui
import psutil

def is_obs_running():
    """Check if OBS is running"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'obs64.exe':
            return True
    return False

def wait_for_obs():
    """Wait for OBS to be running"""
    print("Waiting for OBS to start...")
    while not is_obs_running():
        time.sleep(1)
    print("OBS detected!")
    # Wait extra time for OBS to fully load
    time.sleep(4)

def start_streaming():
    """Click the Start Streaming button"""
    print("Looking for 'Start Streaming' button...")
    
    # Method 1: Try to find the button by image (most reliable)
    # You'll need to take a screenshot of the "Start Streaming" button
    # and save it as 'start_streaming_button.png' in the same directory
    try:
        button_location = pyautogui.locateOnScreen('start_streaming_button.png', confidence=0.8)
        if button_location:
            print(f"Found button at {button_location}")
            pyautogui.click(button_location)
            print("✓ Clicked Start Streaming!")
            return True
    except:
        print("Could not find button by image, trying keyboard shortcut...")
    
    # Method 2: Use keyboard shortcut (if configured in OBS)
    # By default, OBS has no hotkey for Start Streaming
    # You can set one in OBS: File -> Settings -> Hotkeys -> Start Streaming
    # Uncomment and set your hotkey:
    # pyautogui.hotkey('ctrl', 'shift', 's')  # Example
    
    # Method 3: Use menu navigation
    print("Using menu navigation...")
    pyautogui.hotkey('alt', 'c')  # Open Controls menu
    time.sleep(0.3)
    pyautogui.press('s')  # Start Streaming
    print("✓ Sent keyboard commands!")
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("OBS Auto-Start Streaming Script")
    print("=" * 50)
    
    # Launch OBS if not already running
    if not is_obs_running():
        print("Launching OBS...")
        subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])
    
    # Wait for OBS to be ready
    wait_for_obs()
    
    # Start streaming
    start_streaming()
    
    print("\nDone! OBS should now be streaming.")
    print("Check the OBS window to verify.")

if __name__ == "__main__":
    main()
