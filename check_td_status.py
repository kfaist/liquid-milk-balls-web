import pyautogui
import pygetwindow as gw
import time

# Find TouchDesigner window
print("Looking for TouchDesigner window...")
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]

if td_windows:
    td_window = td_windows[0]
    print(f"Found TouchDesigner: {td_window.title}")
    
    # Bring to front
    td_window.activate()
    time.sleep(1)
    print("TouchDesigner window activated")
    
    # Take a focused screenshot
    import mss
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="td_focused.png")
        print(f"Screenshot saved: td_focused.png")
else:
    print("No TouchDesigner window found!")
    print("\nAll windows:")
    for w in gw.getAllWindows():
        if w.title:
            print(f"  - {w.title}")
