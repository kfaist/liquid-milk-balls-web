"""
Configure the WORKING webrender1 operator for LiveKit camera input
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

print("=" * 80)
print("CONFIGURING WORKING WEBRENDER1 FOR LIVEKIT CAMERA INPUT")
print("=" * 80)

# Find and focus TouchDesigner
td_windows = find_td_window()
if not td_windows:
    print("ERROR: TouchDesigner not found!")
    exit(1)

hwnd, title = td_windows[0]
print(f"\nFound: {title}")

# Focus TouchDesigner
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)

# Open Textport
print("Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Clear
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)

print("\nCONFIGURING webrender1 FOR LIVEKIT...")
print("URL: http://localhost:3000/td-auto-viewer.html")

# Script to configure webrender1
script = """wr = op('/webrender1'); wr.par.active = False; import time; time.sleep(0.5); wr.par.active = True; wr.par.url = 'http://localhost:3000/td-auto-viewer.html'; wr.par.reload.pulse(); print('Configured! Waiting 5 seconds...'); time.sleep(5); print('Dimensions:', wr.width, 'x', wr.height)"""

# Type and execute
pyautogui.write(script, interval=0.003)
time.sleep(0.3)
pyautogui.press('enter')

print("\nExecuting configuration (8 seconds)...")
time.sleep(8)

print("\n" + "=" * 80)
print("DONE! Check TouchDesigner webrender1")
print("=" * 80)
