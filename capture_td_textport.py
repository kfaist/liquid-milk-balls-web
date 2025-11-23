"""
Capture TouchDesigner Textport screenshot
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

td_windows = find_td_window()
if td_windows:
    hwnd, title = td_windows[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)

# Take screenshot
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_textport_results.png')
print("Screenshot saved: td_textport_results.png")
