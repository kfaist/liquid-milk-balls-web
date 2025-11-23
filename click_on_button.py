import pyautogui
import time

print("Clicking on 'On' button for Active toggle...")

# The "On" button appears to be at approximately x=1430, y=134
# (slightly to the right of the "Off" position)
x = 1430
y = 134

print(f"Clicking at ({x}, {y})...")
pyautogui.click(x, y)
time.sleep(1)

print("Clicked! Waiting for TouchDesigner to respond...")
time.sleep(2)

print("Taking screenshot to verify...")
