import pyautogui
import time
import pygetwindow as gw

# Find and activate TouchDesigner window
try:
    td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
    if td_windows:
        td_window = td_windows[0]
        td_window.activate()
        time.sleep(1)
        print(f"[OK] Activated TouchDesigner: {td_window.title}")
        
        # Use Ctrl+F to search for operator
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # Type the operator name
        pyautogui.write('webrender_livekit_input', interval=0.05)
        time.sleep(0.5)
        
        # Press Enter to search
        pyautogui.press('enter')
        time.sleep(1)
        
        print("[OK] Searched for webrender_livekit_input operator")
        print("[INFO] TouchDesigner should now show the operator")
        
    else:
        print("[ERROR] TouchDesigner window not found")
except Exception as e:
    print(f"[ERROR] {e}")
