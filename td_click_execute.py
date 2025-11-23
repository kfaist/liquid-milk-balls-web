import pyautogui
import time

print("Moving mouse to TouchDesigner window center...")
# TouchDesigner window is at (0, 0, 3440, 1368)
# Center would be at (1720, 684)
pyautogui.moveTo(1720, 684)
time.sleep(0.5)

print("Clicking to focus...")
pyautogui.click()
time.sleep(1)

print("Sending Alt+T...")
pyautogui.hotkey('alt', 't')
time.sleep(1.5)

print("Clearing...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

print("Typing...")
pyautogui.typewrite("exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py').read())", interval=0.01)
time.sleep(0.5)

print("Executing...")
pyautogui.press('enter')
time.sleep(3)

print("DONE!")
