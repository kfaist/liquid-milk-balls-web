"""
Check WebRender TOP status directly - simpler approach
"""
import pyautogui
import win32gui
import win32con
import time

# Find and focus TouchDesigner
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

print("Finding TouchDesigner...")
td_windows = find_td_window()
if td_windows:
    hwnd, title = td_windows[0]
    print(f"Found: {title}")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)

# Open Textport
print("Opening Textport...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Execute simple status check
print("Checking WebRender status...")
commands = [
    "op('/webrender_livekit_input')",
    "op('/webrender_livekit_input').width",
    "op('/webrender_livekit_input').height",
    "op('/webrender_livekit_input').par.active",
    "op('/webrender_livekit_input').par.url",
]

for cmd in commands:
    pyautogui.write(cmd, interval=0.01)
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(0.5)

print("\nCheck TouchDesigner Textport for output!")
print("Looking for width/height values > 0")

time.sleep(3)
