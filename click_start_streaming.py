import time
import pyautogui

print("Waiting for OBS to fully load...")
time.sleep(8)

print("Moving mouse to Start Streaming button...")
screen_w, screen_h = pyautogui.size()
button_x = int(screen_w * 0.87)
button_y = int(screen_h * 0.75)

pyautogui.moveTo(button_x, button_y, duration=0.5)
time.sleep(0.5)

print(f"Clicking at ({button_x}, {button_y})...")
pyautogui.click()

print("Done! Check OBS - should be streaming now!")
