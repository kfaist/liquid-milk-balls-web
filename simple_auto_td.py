"""
SIMPLE TD AUTOMATION - Click on TD window when prompted
"""
import pyautogui
import time

print("=" * 70)
print("TOUCHDESIGNER AUTO-CONFIGURATION")
print("=" * 70)
print("\nThis will automatically configure TouchDesigner!")
print("\nINSTRUCTIONS:")
print("1. Click on the TouchDesigner window to make it active")
print("2. Come back here and press ENTER")
print("3. The script will do the rest!")
print("=" * 70)

input("\nPress ENTER when TouchDesigner is the active window...")

print("\nStarting in 3 seconds...")
time.sleep(1)
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)

# Open textport with Alt+T
print("\nOpening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Clear any existing text
print("Clearing textport...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.press('delete')
time.sleep(0.5)

# The configuration command
command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"

print("\nTyping configuration command...")
for char in command:
    pyautogui.press(char)
    time.sleep(0.01)

time.sleep(1)

# Press Enter to execute
print("\nExecuting command...")
pyautogui.press('enter')
time.sleep(3)

print("\n" + "=" * 70)
print("CONFIGURATION COMMAND EXECUTED!")
print("=" * 70)
print("\nCheck the TouchDesigner textport for results.")
print("\nIf successful, you should see configuration messages.")
print("\nNext steps:")
print("1. Look for 'Web Render TOP' in TouchDesigner")
print("2. Open publisher.html (Firefox tab)")
print("3. Click 'Start Publishing'")
print("4. Video should appear in TD!")
print("=" * 70)

input("\nPress ENTER to close...")
