import pyautogui
import time
import subprocess

print("REFRESHING PUBLISHER AND STARTING STREAM...")

# Click on browser area (middle of screen)
pyautogui.click(800, 400)
time.sleep(0.3)

# F5 to refresh
pyautogui.press('f5')
print("Refreshed publisher page...")
time.sleep(3)

# Look for and click "Start Publishing" button
# Try clicking in the center-ish area where button usually is
pyautogui.click(400, 300)
time.sleep(1)

print("DONE! Check TouchDesigner for video!")
