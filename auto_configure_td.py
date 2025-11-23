"""
FULL AUTO TOUCHDESIGNER CONFIGURATION
This will click into TD and configure everything automatically
"""
import pyautogui
import win32gui
import win32con
import time

print("=" * 70)
print("AUTOMATIC TOUCHDESIGNER CONFIGURATION STARTING")
print("=" * 70)

# Find TouchDesigner window
def find_td_window():
    windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "TouchDesigner" in window_text and "ndi-stream" in window_text:
                windows.append((hwnd, window_text))
        return True
    win32gui.EnumWindows(callback, None)
    return windows

print("\nSearching for TouchDesigner window...")
td_windows = find_td_window()

if not td_windows:
    print("ERROR: TouchDesigner window not found!")
    print("Make sure ndi-streamCOPY.toe is open")
    input("Press ENTER to exit...")
    exit()

hwnd, title = td_windows[0]
print(f"Found: {title}")

# Bring TouchDesigner to front
print("\nBringing TouchDesigner to foreground...")
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(2)

# Get window position
rect = win32gui.GetWindowRect(hwnd)
x, y, x2, y2 = rect
center_x = (x + x2) // 2
center_y = (y + y2) // 2

print(f"Window at: {x}, {y} to {x2}, {y2}")

# Click into the window
print("\nClicking into TouchDesigner window...")
pyautogui.click(center_x, center_y)
time.sleep(1)

# Open textport with Alt+T
print("\nOpening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# The configuration command
command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"

print("\nTyping configuration command...")
print(f"Command: {command}")
pyautogui.typewrite(command, interval=0.02)
time.sleep(1)

# Press Enter to execute
print("\nExecuting command (pressing ENTER)...")
pyautogui.press('enter')
time.sleep(3)

print("\n" + "=" * 70)
print("CONFIGURATION COMMAND SENT!")
print("=" * 70)
print("\nCheck TouchDesigner textport output to see if configuration worked.")
print("\nIf successful, you should see:")
print("  - Web Render TOP found or created")
print("  - Parameters configured")
print("  - Ready to receive video!")
print("\nNext: Open publisher.html and click 'Start Publishing'")
print("=" * 70)

input("\nPress ENTER to exit...")
