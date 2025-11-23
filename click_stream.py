import pyautogui
import time

print("Clicking Start Streaming in OBS...")

# Get screen size
screen_w, screen_h = pyautogui.size()

# OBS Start Streaming button location
button_x = int(screen_w * 0.87)
button_y = int(screen_h * 0.75)

print(f"Moving to ({button_x}, {button_y})...")
pyautogui.moveTo(button_x, button_y, duration=0.3)
time.sleep(0.3)

print("Clicking...")
pyautogui.click()

print("DONE! Check OBS - should be streaming now!")
