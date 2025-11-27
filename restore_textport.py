import pyautogui
import pygetwindow as gw
import ctypes
import time

# Find Textport window
textport_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if textport_windows:
    tp = textport_windows[0]
    
    # Restore/maximize it
    try:
        tp.restore()
        time.sleep(0.3)
        tp.activate()
        time.sleep(0.5)
    except:
        # Use Windows API directly
        SW_RESTORE = 9
        ctypes.windll.user32.ShowWindow(tp._hWnd, SW_RESTORE)
        time.sleep(0.3)
        ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
        time.sleep(0.5)
    
    print(f'Textport restored, now at ({tp.left}, {tp.top})')
    
    # Take screenshot
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/textport_restored.png')
    print('Screenshot saved')
else:
    print('Textport not found')
