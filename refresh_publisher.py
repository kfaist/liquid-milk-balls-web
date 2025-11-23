import pyautogui
import time

print("Refreshing publisher page...")

# Simple F5 to refresh current tab
pyautogui.press('f5')
time.sleep(2)

print("Publisher page refreshed!")
print("Look for 'Start Publishing' button")
