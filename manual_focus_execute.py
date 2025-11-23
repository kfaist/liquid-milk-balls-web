import subprocess
import time

# Start a new command prompt that will send keys to TouchDesigner
script = '''
import pyautogui
import time

# Wait for TouchDesigner focus
time.sleep(3)

# Open textport
pyautogui.press('f8')  # Try F8 which might be textport shortcut
time.sleep(1)

if not worked:
    pyautogui.hotkey('alt', 't')
    time.sleep(1)

# Type command
cmd = """exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py').read())"""
for char in cmd:
    pyautogui.press(char)
    time.sleep(0.01)

time.sleep(0.5)
pyautogui.press('enter')
'''

with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/temp_execute.py', 'w') as f:
    f.write(script)

# Tell user to focus TD
print("=" * 60)
print("INSTRUCTIONS:")
print("=" * 60)
print("1. Click on TouchDesigner window NOW")
print("2. You have 3 seconds...")
time.sleep(3)
print("3. Sending commands...")

subprocess.run(['python', 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/temp_execute.py'])
