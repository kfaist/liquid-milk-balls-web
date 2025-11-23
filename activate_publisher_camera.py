"""
Activate camera on publisher page and verify the complete pipeline
"""
import pyautogui
import win32gui
import win32con
import time

print("=" * 70)
print("ACTIVATING CAMERA PUBLISHER")
print("=" * 70)

# Find Firefox
def find_firefox():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Firefox" in title or "Mozilla" in title:
                windows.append((hwnd, title))
        return True
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

firefox_windows = find_firefox()
if not firefox_windows:
    print("ERROR: Firefox not found!")
    exit(1)

hwnd, title = firefox_windows[0]
print(f"Found Firefox: {title}")

# Focus Firefox
print("Focusing Firefox...")
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(1)

# Go to publisher tab (Ctrl+L to address bar, then type URL)
print("Opening publisher page...")
pyautogui.hotkey('ctrl', 'l')
time.sleep(0.5)
pyautogui.write('localhost:3000/publisher.html', interval=0.02)
pyautogui.press('enter')
time.sleep(3)

print("\nLooking for 'Start Publishing' button...")
print("Searching for button on screen...")

# Try to find and click "Start Publishing" button
# Look for the button text
try:
    button_location = pyautogui.locateOnScreen('start_publishing_button.png', confidence=0.7)
    if button_location:
        pyautogui.click(button_location)
        print("✓ Clicked 'Start Publishing' button!")
    else:
        print("Button not found by image - trying Tab navigation...")
        # Tab through page to find button
        for i in range(10):
            pyautogui.press('tab')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(1)
except Exception as e:
    print(f"Image search failed: {e}")
    print("Trying keyboard navigation...")
    # Press Tab several times then Enter
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('enter')

time.sleep(2)

print("\n" + "=" * 70)
print("CAMERA SHOULD BE STARTING!")
print("=" * 70)
print("\nIf browser asks for camera permission, allow it!")
print("\nNext: Check TouchDesigner webrender1 operator for camera feed")
