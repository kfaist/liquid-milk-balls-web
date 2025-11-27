import pyautogui
import pygetwindow as gw
import ctypes
import time

# Find Textport and minimize it
tp_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if tp_windows:
    tp = tp_windows[0]
    tp.minimize()
    print('Textport minimized')
    time.sleep(0.5)

# Find and activate TouchDesigner
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title and 'ndi-streamCOPY' in w.title]
if td_windows:
    td = td_windows[0]
    ctypes.windll.user32.SetForegroundWindow(td._hWnd)
    time.sleep(0.5)
    
    # Press H to go home/fit all
    pyautogui.press('h')
    time.sleep(0.5)
    
    # Take screenshot
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_main_view.png', region=(0, 0, 1600, 900))
    print('TD main view saved')
