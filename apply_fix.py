import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Fix command for WebRender
cmd = """op('/webrender1').par.url = 'http://localhost:3000/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
print('WebRender URL fixed and reloaded!')"""

pyperclip.copy(cmd)

# Find Textport
tp_windows = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp_windows:
    tp = tp_windows[0]
    ctypes.windll.user32.ShowWindow(tp._hWnd, 9)  # Restore
    time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1.5)
    
    # Capture result
    region = (tp.left, tp.top, min(tp.width, 1200), min(tp.height, 700))
    if region[0] >= 0 and region[1] >= 0:
        pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_result.png', region=region)
    print('Fix applied!')
else:
    print('Textport not found')
