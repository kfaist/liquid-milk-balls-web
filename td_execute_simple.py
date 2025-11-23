import pyautogui
import time

print("Switching to TouchDesigner...")
# Alt+Tab to switch to TD
pyautogui.hotkey('alt', 'tab')
time.sleep(0.5)

# Click in the textport (bottom part of window)
print("Clicking in textport...")
screen_width, screen_height = pyautogui.size()
# Click in bottom left area where textport usually is
pyautogui.click(250, screen_height - 100)
time.sleep(0.3)

# Clear any existing text in textport
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.1)

# Paste the script
print("Pasting script...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

# Press Enter to execute
print("Executing...")
pyautogui.press('enter')
time.sleep(1)

print("Done! Taking screenshot to see results...")
