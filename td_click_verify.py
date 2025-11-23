import pyautogui
import time

time.sleep(2)
pyautogui.moveTo(1720, 684)
time.sleep(0.3)
pyautogui.click()
time.sleep(0.8)
pyautogui.hotkey('alt', 't')
time.sleep(1)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.typewrite("exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verify_to_file.py').read())", interval=0.01)
time.sleep(0.4)
pyautogui.press('enter')
time.sleep(2)
print("Verify sent!")
