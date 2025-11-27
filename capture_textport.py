import pyautogui
import pygetwindow as gw
import ctypes
import time

# Find and activate Textport window
textport_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if textport_windows:
    tp = textport_windows[0]
    print(f'Found Textport at ({tp.left}, {tp.top}), size {tp.width}x{tp.height}')
    
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    # Take screenshot
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/textport_view.png')
    print('Textport screenshot saved')
else:
    print('Textport not found')
