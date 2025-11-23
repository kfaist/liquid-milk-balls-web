import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False

print("ACTIVATING PUBLISHER CAMERA...")

# Find Firefox
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title or 'Mozilla' in w.title]
if firefox_windows:
    ff = firefox_windows[0]
    print(f"Found Firefox: {ff.title}")
    
    # Click Firefox
    center_x = ff.left + (ff.width // 2)
    center_y = ff.top + (ff.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)
    
    # Switch to first tab (might be publisher)
    print("Switching tabs...")
    pyautogui.hotkey('ctrl', '1')
    time.sleep(1)
    
    # Try to click Start Camera button (middle of page, upper area)
    button_x = ff.left + (ff.width // 2)
    button_y = ff.top + 250
    
    print("Clicking Start Camera button area...")
    pyautogui.click(button_x, button_y)
    time.sleep(2)
    
    print("[OK] Camera start attempted!")
    
    # Take screenshot to verify
    screenshot = pyautogui.screenshot()
    screenshot.save('publisher_activated.png')
    print("[SCREENSHOT] publisher_activated.png saved")
else:
    print("[ERROR] Firefox not found!")
