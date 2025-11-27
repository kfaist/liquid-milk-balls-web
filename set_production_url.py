import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Set production URL for WebRender
cmd = """wr = op('/webrender1')
wr.par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html'
wr.par.reload.pulse()
print('URL set to PRODUCTION:', wr.par.url.val)
print('Resolution:', wr.width, 'x', wr.height)"""

pyperclip.copy(cmd)

# Find and use Textport
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
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/final_config.png')
    print('Done - check final_config.png')
