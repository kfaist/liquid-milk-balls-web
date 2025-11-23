import pyautogui
import time
import pyperclip

# The command to execute in TD textport
td_command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_activate_specific.py').read())"

print("Activating TouchDesigner...")
print("1. Finding TouchDesigner window...")

# Find and focus TouchDesigner window
windows = pyautogui.getWindowsWithTitle('TouchDesigner')
if windows:
    td_window = windows[0]
    td_window.activate()
    time.sleep(0.5)
    print("   [OK] TouchDesigner focused")
    
    # Open textport with Alt+T
    print("2. Opening textport (Alt+T)...")
    pyautogui.hotkey('alt', 't')
    time.sleep(0.5)
    
    # Copy command to clipboard
    pyperclip.copy(td_command)
    print("3. Pasting activation command...")
    time.sleep(0.3)
    
    # Paste with Ctrl+V
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Press Enter to execute
    print("4. Executing...")
    pyautogui.press('enter')
    time.sleep(1)
    
    print("\n[OK] Command executed in TouchDesigner!")
    print("\nNow checking the textport output...")
    print("Look at TouchDesigner textport for activation results.")
    
else:
    print("ERROR: Could not find TouchDesigner window")
    print("Make sure TouchDesigner is running")
