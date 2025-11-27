import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Set production URL for WebRender
cmd = """wr = op('/webrender1')
if wr:
    wr.par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html'
    wr.par.mediastream = True
    wr.par.reload.pulse()
    print('URL:', wr.par.url.val)
    print('MediaStream:', wr.par.mediastream.val)
    print('Size:', wr.width, 'x', wr.height)
else:
    print('webrender1 not found!')"""

pyperclip.copy(cmd)

# Open textport
td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td:
    ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
    time.sleep(0.3)
    pyautogui.hotkey('alt', 't')
    time.sleep(1)

tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Capture textport result
    t = tp[0]
    if t.left >= 0:
        pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/wr_configured.png', 
                            region=(t.left, t.top, min(t.width, 1000), min(t.height, 500)))
print('Done')
