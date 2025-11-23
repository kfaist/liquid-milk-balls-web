"""
Execute webrender1 configuration in TouchDesigner Textport
CAREFULLY - Close other windows first!
"""
import pyautogui
import win32gui
import win32con
import time

print("Step 1: Finding and closing Claude chat window...")
def find_window(title_contains):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_contains.lower() in title.lower():
                windows.append((hwnd, title))
        return True
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# Find and close Claude window
claude_windows = find_window("Claude")
for hwnd, title in claude_windows:
    if "Control" in title or "Alt" in title:  # This is our chat
        print(f"Closing: {title}")
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        time.sleep(1)

print("\nStep 2: Finding TouchDesigner window...")
td_windows = find_window("TouchDesigner")
if not td_windows:
    print("ERROR: TouchDesigner not found!")
    exit(1)

hwnd, title = td_windows[0]
print(f"Found: {title}")

# Bring TouchDesigner to foreground
print("\nStep 3: Focusing TouchDesigner...")
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
time.sleep(0.5)
win32gui.SetForegroundWindow(hwnd)
time.sleep(2)

# Click in the center of TouchDesigner window to ensure focus
rect = win32gui.GetWindowRect(hwnd)
center_x = (rect[0] + rect[2]) // 2
center_y = (rect[1] + rect[3]) // 2
pyautogui.click(center_x, center_y)
time.sleep(1)

print("\nStep 4: Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

print("\nStep 5: Executing webrender1 configuration...")
# Clear textport
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)

# Type the configuration command
cmd = "wr=op('/webrender1');wr.par.active=0;import time;time.sleep(0.5);wr.par.active=1;wr.par.url='http://localhost:3000/td-auto-viewer.html';wr.par.reload.pulse();time.sleep(5);print('CONFIGURED:',wr.width,'x',wr.height)"
pyautogui.write(cmd, interval=0.003)
time.sleep(0.5)

# Execute
pyautogui.press('enter')
print("Command sent! Waiting 8 seconds...")
time.sleep(8)

print("\nDONE! Check TouchDesigner Textport for results.")
