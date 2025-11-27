import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

cmd = """op('/webrender1').par.url = 'https://adequate-balance-production.up.railway.app/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
print('URL set to:', op('/webrender1').par.url.val)"""

pyperclip.copy(cmd)

td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td:
    ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
    time.sleep(0.3)
    pyautogui.hotkey('alt', 't')
    time.sleep(0.8)

tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
print('Done - WebRender URL updated!')
