import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Command to fix the WebRender URL
cmd = """op('/webrender1').par.url = 'http://localhost:3000/td-input-viewer.html'
op('/webrender1').par.reload.pulse()
print('URL changed to td-input-viewer.html and reloaded!')"""

pyperclip.copy(cmd)
print('Copied fix command')

# Find and activate Textport
tp_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if tp_windows:
    tp = tp_windows[0]
    # Restore if minimized
    if tp.left < 0:
        ctypes.windll.user32.ShowWindow(tp._hWnd, 9)
        time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)
    
    print('Executed!')
else:
    print('Open Textport (Dialogs > Textport) and paste this:')
    print(cmd)
