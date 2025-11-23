import pyautogui
import subprocess
import time

print("Activating TouchDesigner window...")

# Activate TouchDesigner
subprocess.run(['powershell',
    'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
    '[Microsoft.VisualBasic.Interaction]::AppActivate("TouchDesigner")'],
    shell=True)

time.sleep(2)

print("Taking screenshot of TouchDesigner...")
screenshot = pyautogui.screenshot()
screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\touchdesigner_screenshot.png')
print("Screenshot saved to: touchdesigner_screenshot.png")

# Also try to find webrender operator by searching for it
print("\nLooking for webrender_livekit_input operator...")
try:
    # Take a screenshot and look for specific text/colors
    screenshot = pyautogui.screenshot()
    # Save it
    screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td_active_window.png')
    print("Active window screenshot saved!")
except Exception as e:
    print(f"Error: {e}")
