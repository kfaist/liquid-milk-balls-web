import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# The CORRECT production URL
prod_url = "https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html"

cmd = f"""op('/webrender1').par.url = '{prod_url}'
op('/webrender1').par.reload.pulse()
print('URL set to PRODUCTION:', op('/webrender1').par.url.val)"""

pyperclip.copy(cmd)

# Find and activate Textport
tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.ShowWindow(tp[0]._hWnd, 9)
    time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Screenshot textport
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/prod_url_set.png')
    print('Production URL set!')
else:
    # Try to open textport
    td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
    if td:
        ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
        time.sleep(0.3)
        pyautogui.hotkey('alt', 't')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/prod_url_set.png')
        print('Production URL set via new textport!')
