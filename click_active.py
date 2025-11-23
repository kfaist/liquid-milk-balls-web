import pyautogui
import time

print("Finding Active toggle...")

# Based on screenshot, the Active toggle is at approximately:
# Right side panel, near the top, after "Web Render" header
# Coordinates roughly: x=1390, y=134

x = 1390
y = 134

print(f"Clicking Active toggle at ({x}, {y})...")
pyautogui.click(x, y)
time.sleep(0.5)

print("Active toggle clicked! Taking screenshot to verify...")
