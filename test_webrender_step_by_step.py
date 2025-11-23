"""
WebRender Diagnostic - Test with simple page first
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

print("=" * 70)
print("WEBRENDER DIAGNOSTIC - Testing with simple page")
print("=" * 70)

# Find TouchDesigner
td_windows = find_td_window()
if not td_windows:
    print("ERROR: TouchDesigner not found!")
    exit(1)

hwnd, title = td_windows[0]
print(f"Found: {title}")

# Focus TouchDesigner
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)

# Open Textport
print("Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Clear any existing text
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)

print("\nStep 1: Testing with SIMPLE page first...")
print("URL: http://localhost:3000/simple-test.html")

# Configure WebRender with simple test page
script = """
wr = op('/webrender_livekit_input')
wr.par.active = False
import time; time.sleep(0.5)
wr.par.active = True
wr.par.url = 'http://localhost:3000/simple-test.html'
wr.par.reload.pulse()
import time; time.sleep(3)
print('WebRender dimensions:', wr.width, 'x', wr.height)
if wr.width > 0:
    print('SUCCESS! WebRender is working!')
else:
    print('FAILED - WebRender not loading page')
"""

pyautogui.write(script.replace('\n', '; '), interval=0.005)
time.sleep(0.3)
pyautogui.press('enter')

print("\nWaiting for test to complete (5 seconds)...")
time.sleep(5)

print("\n" + "=" * 70)
print("Check TouchDesigner Textport window for results!")
print("=" * 70)
print("\nIf you see 'SUCCESS! WebRender is working!' then:")
print("  → WebRender can load pages")
print("  → Next step: Try td-auto-viewer.html")
print("\nIf you see 'FAILED':")
print("  → WebRender has a deeper issue")
print("  → Will try alternative methods")
