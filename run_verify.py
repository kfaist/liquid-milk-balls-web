import pyautogui
import pyperclip
import time

pyautogui.FAILSAFE = False

with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/verify_and_configure_webrender.py', 'r') as f:
    script = f.read()

pyperclip.copy(script)
time.sleep(0.5)
pyautogui.hotkey('alt', 't')
time.sleep(1)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.press('delete')
time.sleep(0.2)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.hotkey('ctrl', 'enter')
time.sleep(2)
print("Script executed. Check webrender_config_output.txt for results")
