"""
Capture OBS window to see what's happening
"""
import pyautogui
import win32gui
import win32con
import time

def find_obs_window():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "OBS" in title:
                windows.append((hwnd, title))
        return True
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# Find OBS
obs_windows = find_obs_window()
if obs_windows:
    hwnd, title = obs_windows[0]
    print(f"Found OBS: {title}")
    
    # Focus OBS
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.5)
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass
    
    time.sleep(1)

# Capture
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/obs_capture.png')
print("Screenshot saved: obs_capture.png")
