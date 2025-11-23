"""
Activate TouchDesigner and take screenshot to verify webrender
"""
import pyautogui
import time

print("Step 1: Activating TouchDesigner...")

# Click on TouchDesigner in taskbar (approximate position)
# Taskbar is at bottom, TouchDesigner likely on right side
pyautogui.click(x=970, y=639)  # Near middle-right of taskbar
time.sleep(2)

# Take screenshot
print("Step 2: Taking screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td_view.png')

print("[OK] TouchDesigner activated and screenshot saved!")
print("File: td_view.png")
