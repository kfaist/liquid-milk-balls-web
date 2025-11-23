import pyautogui
import time
import pygetwindow as gw

# Find TouchDesigner window
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    td_window = td_windows[0]
    print(f"Found TouchDesigner: {td_window.title}")
    
    # Activate window
    td_window.activate()
    time.sleep(0.5)
    
    # Click in textport area (bottom left of TD window)
    # Approximate coordinates based on screenshot
    x = td_window.left + 250
    y = td_window.bottom - 100
    
    print(f"Clicking at ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(0.3)
    
    # Paste the script
    print("Pasting script...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # Press Enter to execute
    print("Executing...")
    pyautogui.press('enter')
    time.sleep(1)
    
    print("Done! Check TouchDesigner textport for results.")
else:
    print("TouchDesigner window not found!")
