import pyautogui
import time

time.sleep(2)
print("Verifying...")
pyautogui.hotkey('alt', 't')
time.sleep(0.8)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.write("exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verify_to_file.py').read())", interval=0.005)
time.sleep(0.4)
pyautogui.press('enter')
time.sleep(2)
print("Verification sent!")
