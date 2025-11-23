"""
Minimize Claude window and take clear screenshot of TouchDesigner
"""
import pyautogui
import time

print("Step 1: Minimizing Claude window...")
# Click minimize button on Claude window (top right area)
pyautogui.click(x=919, y=91)  # Minimize button
time.sleep(1)

print("Step 2: Taking screenshot of TouchDesigner...")
screenshot = pyautogui.screenshot()
screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td_clear.png')

print("[OK] Screenshot saved: td_clear.png")
