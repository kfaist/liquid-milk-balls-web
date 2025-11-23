"""
Take screenshots of current system state
"""
import pyautogui
import time

print("Taking system screenshots...")

# Screenshot 1: Full desktop
print("1. Full desktop view...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/system_state_full.png')

time.sleep(2)

# Screenshot 2: Browser window
print("2. Focusing browser...")
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/browser_state.png')

print("\nScreenshots saved:")
print("- system_state_full.png")
print("- browser_state.png")
