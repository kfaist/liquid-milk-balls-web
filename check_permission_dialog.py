"""
Capture full desktop and look for camera permission dialog
"""
import pyautogui
import time

print("Capturing full desktop...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/desktop_full.png')
print("Desktop screenshot saved: desktop_full.png")

print("\nLooking for 'Allow' button for camera permission...")
time.sleep(1)

# Try to find "Allow" button if permission dialog is showing
try:
    allow_button = pyautogui.locateCenterOnScreen('allow', confidence=0.6)
    if allow_button:
        print(f"Found 'Allow' button at {allow_button}")
        pyautogui.click(allow_button)
        print("Clicked 'Allow'!")
        time.sleep(2)
    else:
        print("No 'Allow' button found - may have already been granted")
except:
    print("Could not auto-detect Allow button")
    print("Check desktop_full.png to see current state")
