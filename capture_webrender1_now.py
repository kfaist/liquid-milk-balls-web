"""
Capture TouchDesigner screen to verify webrender1 configuration
"""
import pyautogui
import win32gui
import win32con
import time

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

# Find and focus TouchDesigner
td_windows = find_td_window()
if td_windows:
    hwnd, title = td_windows[0]
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.5)
    except:
        pass
    time.sleep(1)

# Take screenshot
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrender1_configured.png')
print("Screenshot saved: webrender1_configured.png")
