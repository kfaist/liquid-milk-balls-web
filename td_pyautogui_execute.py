import pyautogui
import time
from PIL import ImageGrab

print("="*60)
print("TOUCHDESIGNER WINDOW SCREENSHOT")
print("="*60)

# Take screenshot
time.sleep(1)
screenshot = ImageGrab.grab()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_screenshot.png')
print(f"Screenshot saved: td_screenshot.png")
print(f"Screen size: {screenshot.size}")

# Try to click on TouchDesigner window
# First, let's find windows
import win32gui

def callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if 'TouchDesigner' in title:
            rect = win32gui.GetWindowRect(hwnd)
            windows.append({
                'hwnd': hwnd,
                'title': title,
                'rect': rect
            })
    return True

windows = []
win32gui.EnumWindows(callback, windows)

if windows:
    td_win = windows[0]
    print(f"\nFound TouchDesigner: {td_win['title']}")
    print(f"Position: {td_win['rect']}")
    
    # Focus the window
    win32gui.SetForegroundWindow(td_win['hwnd'])
    time.sleep(0.5)
    
    # Open textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Type the command
    cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_FINAL.py').read())"
    pyautogui.typewrite(cmd, interval=0.01)
    time.sleep(0.5)
    
    # Press enter
    pyautogui.press('enter')
    time.sleep(2)
    
    print("\n✅ Command sent via PyAutoGUI!")
else:
    print("\n❌ TouchDesigner window not found")
