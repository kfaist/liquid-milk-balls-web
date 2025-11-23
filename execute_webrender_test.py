"""
Execute systematic WebRender test in TouchDesigner
"""
import pyautogui
import win32gui
import win32con
import time
import sys

# Find TouchDesigner window
def find_td_window():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "TouchDesigner" in title:
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

print("Finding TouchDesigner window...")
td_windows = find_td_window()

if not td_windows:
    print("ERROR: TouchDesigner window not found!")
    print("Make sure TouchDesigner is running.")
    sys.exit(1)

hwnd, title = td_windows[0]
print(f"Found: {title}")

# Focus TouchDesigner
print("Focusing TouchDesigner...")
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)

# Open Textport (Alt+T)
print("Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(1.5)

# Type the command to execute the systematic test
print("Executing systematic WebRender test...")
command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/systematic_webrender_test.py').read())"

# Clear any existing text
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)

# Type the command
pyautogui.write(command, interval=0.01)
time.sleep(0.5)

# Press Enter to execute
pyautogui.press('enter')

print("\n" + "=" * 70)
print("COMMAND EXECUTED!")
print("=" * 70)
print("\nSwitch to TouchDesigner Textport to see test results.")
print("\nThe test will:")
print("1. Test simple gradient page")
print("2. Test green background page")
print("3. Test LiveKit viewer page")
print("\nResults will appear in the Textport window.")
print("\nLeave this window open while checking TouchDesigner.")

# Keep script running so user can see the message
input("\nPress Enter when you've reviewed the results in TouchDesigner...")
