import pyautogui
import pygetwindow as gw
import ctypes
import time

# Find and activate Textport window
tp_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if tp_windows:
    tp = tp_windows[0]
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    # Press Enter twice to complete the loop
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    
    # Capture result
    region = (tp.left, tp.top, tp.width, tp.height)
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/textport_result.png', region=region)
    print('Captured result')
else:
    print('Textport not found')
