import pyautogui
import time

print("="*60)
print("TOUCHDESIGNER DIRECT AUTOMATION")
print("="*60)

# Just send the keystrokes - assuming TD is already focused
print("\nWaiting 2 seconds for TD to be in focus...")
time.sleep(2)

print("Sending Alt+T...")
pyautogui.hotkey('alt', 't')
time.sleep(1)

print("Clearing textport...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

print("Typing command...")
cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py').read())"
pyautogui.write(cmd, interval=0.005)
time.sleep(0.5)

print("Executing...")
pyautogui.press('enter')
time.sleep(3)

print("\n" + "="*60)
print("DONE! Check TouchDesigner textport")
print("="*60)
