import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

cmd = """op('/webrender1').par.reload.pulse()
print('WebRender reloaded!')"""

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
    time.sleep(3)

# Screenshot TD
td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td:
    ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
    time.sleep(0.5)
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/wr_reloaded.png')
print('Done')
