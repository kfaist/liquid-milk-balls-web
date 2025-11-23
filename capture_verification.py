import pyautogui
import pygetwindow as gw
import time

print("Step 1: Switching to Firefox...")
# Find Firefox window
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title or 'Mozilla' in w.title]
if firefox_windows:
    firefox = firefox_windows[0]
    firefox.activate()
    time.sleep(0.5)
    print(f"Firefox activated: {firefox.title}")
    
    # Press F12 to open DevTools
    print("\nStep 2: Opening Developer Console (F12)...")
    pyautogui.press('f12')
    time.sleep(1)
    
    print("\nStep 3: Taking screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save('firefox_console.png')
    print(f"Screenshot saved: firefox_console.png")
    
    # Also check what tab is active
    print(f"\nCurrent Firefox tab: {firefox.title}")
else:
    print("Firefox not found!")

print("\n\nStep 4: Switching to TouchDesigner...")
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    td = td_windows[0]
    td.activate()
    time.sleep(1)
    print(f"TouchDesigner activated: {td.title}")
    
    print("\nStep 5: Taking TouchDesigner screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save('touchdesigner_view.png')
    print(f"Screenshot saved: touchdesigner_view.png")
else:
    print("TouchDesigner not found!")

print("\n✅ Verification screenshots captured!")
print("   - firefox_console.png")
print("   - touchdesigner_view.png")
