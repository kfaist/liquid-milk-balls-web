"""
Quick automation to fix WebRender TOP URL
"""
import pyautogui
import pyperclip
import time

# Disable failsafe
pyautogui.FAILSAFE = False

print("Reading quick fix script...")
with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/quick_fix_webrender.py', 'r') as f:
    script = f.read()

print("Copying to clipboard...")
pyperclip.copy(script)

print("Opening textport...")
time.sleep(0.5)
pyautogui.hotkey('alt', 't')
time.sleep(1)

print("Pasting script...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

print("Executing...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'enter')
time.sleep(1)

print("Done! Check TouchDesigner textport for results.")
