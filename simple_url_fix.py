import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Simple direct command
cmd = """op('/webrender1').par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
print('URL set to td-input-viewer.html')"""

pyperclip.copy(cmd)

tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Now take screenshot of TD to see result
    td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
    if td:
        ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
        time.sleep(0.5)
        pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/after_url_change.png')
        print('Done')
