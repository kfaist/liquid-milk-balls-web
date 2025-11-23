"""
Direct TouchDesigner Configuration
Simple keystroke automation
"""
import pyautogui
import pyperclip
import time

print("=" * 70)
print("CONFIGURING TOUCHDESIGNER NOW!")
print("=" * 70)
print("\nMake sure TouchDesigner window is visible!")
print("Starting in 3 seconds...")
time.sleep(3)

# Command to execute
command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"

print("\n1. Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(1.5)

print("2. Copying command to clipboard...")
pyperclip.copy(command)
time.sleep(0.3)

print("3. Pasting command (Ctrl+V)...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

print("4. Executing (ENTER)...")
pyautogui.press('enter')
time.sleep(2)

print("\n" + "=" * 70)
print("DONE! Check TouchDesigner Textport for results!")
print("=" * 70)
print("\nThe configuration script has been executed.")
print("Look at the Textport to see if configuration succeeded.")
print("\nIf it worked, you should see:")
print("  - Found or created Web Render TOP")
print("  - Configured parameters")
print("  - Ready to receive video!")
print("\nNext: Test with publisher.html in Firefox!")
print("=" * 70)
