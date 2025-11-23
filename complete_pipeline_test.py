"""
Complete End-to-End Pipeline Test
"""
import pyautogui
import win32gui
import win32con
import time

print("=" * 70)
print("COMPLETE PIPELINE TEST")
print("=" * 70)

def find_window(keyword):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if keyword.lower() in title.lower():
                windows.append((hwnd, title))
        return True
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# Step 1: Check TouchDesigner webrender1
print("\n[1/5] Checking TouchDesigner webrender1...")
td_windows = find_window("TouchDesigner")
if td_windows:
    hwnd, title = td_windows[0]
    print(f"  [OK] Found: {title}")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # Check webrender1 status
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    pyautogui.write("print('webrender1 URL:', op('/webrender1').par.url.val); print('Size:', op('/webrender1').width, 'x', op('/webrender1').height)", interval=0.01)
    pyautogui.press('enter')
    time.sleep(1)
else:
    print("  [FAIL] TouchDesigner not found!")

# Step 2: Take screenshot of current state
print("\n[2/5] Capturing current TouchDesigner state...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_current_state.png')
print("  [OK] Saved: td_current_state.png")

# Step 3: Open Firefox to publisher page
print("\n[3/5] Opening Firefox publisher page...")
firefox_windows = find_window("Firefox")
if firefox_windows:
    hwnd, title = firefox_windows[0]
    print(f"  [OK] Found: {title}")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # Navigate to publisher
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    pyautogui.write('localhost:3000/publisher.html', interval=0.02)
    pyautogui.press('enter')
    time.sleep(3)
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/publisher_page.png')
    print("  [OK] Saved: publisher_page.png")
else:
    print("  [FAIL] Firefox not found!")

# Step 4: Wait for manual interaction
print("\n[4/5] Waiting for manual camera activation...")
print("  Please click 'Start Publishing' button if visible")
print("  Waiting 5 seconds...")
time.sleep(5)

# Step 5: Check result in TouchDesigner
print("\n[5/5] Checking result in TouchDesigner...")
if td_windows:
    hwnd, title = td_windows[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # Take final screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_final_check.png')
    print("  [OK] Saved: td_final_check.png")

print("\n" + "=" * 70)
print("TEST COMPLETE!")
print("=" * 70)
print("\nScreenshots saved:")
print("  1. td_current_state.png - TouchDesigner before test")
print("  2. publisher_page.png - Publisher page in Firefox")
print("  3. td_final_check.png - TouchDesigner after test")
print("\nNext: Review screenshots to verify camera feed!")
