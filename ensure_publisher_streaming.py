import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False

print("="*70)
print("ENSURING PUBLISHER IS STREAMING")
print("="*70)

# Find Firefox
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title]
if firefox_windows:
    ff = firefox_windows[0]
    
    # Activate Firefox
    ff_x = ff.left + ff.width // 2
    ff_y = ff.top + ff.height // 2
    pyautogui.click(ff_x, ff_y)
    time.sleep(0.5)
    
    print("[OK] Firefox activated")
    
    # Open publisher in new tab
    print("\n[ACTION] Opening publisher page...")
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
    
    url = "localhost:3000/publisher.html"
    pyautogui.write(url, interval=0.02)
    pyautogui.press('enter')
    time.sleep(3)
    
    print("[OK] Publisher page loaded")
    
    # Click Start Camera button (center-upper area)
    print("\n[ACTION] Clicking Start Camera...")
    button_x = ff.left + ff.width // 2
    button_y = ff.top + 250
    pyautogui.click(button_x, button_y)
    time.sleep(3)
    
    print("[OK] Start Camera clicked")
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('publisher_camera_active.png')
    print("[SCREENSHOT] publisher_camera_active.png")
    
    print("\n" + "="*70)
    print("PUBLISHER CAMERA ACTIVATED!")
    print("="*70)
    print("\nNow the full pipeline should work:")
    print("Publisher → LiveKit → TD Viewer → TouchDesigner")
    print("\nWait 10 seconds, then check TouchDesigner webrender!")
    print("="*70)
    
else:
    print("[ERROR] Firefox not found!")
