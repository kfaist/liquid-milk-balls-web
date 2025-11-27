import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# The command to find media-related parameters
cmd = """for p in wr.pars():
    if 'media' in p.name.lower() or 'audio' in p.name.lower():
        print(f"{p.name} = {p.val}")"""

# Copy to clipboard
pyperclip.copy(cmd)
print('Copied search command to clipboard')

# Find and activate Textport window
tp_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if tp_windows:
    tp = tp_windows[0]
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    # Paste
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # Press Enter to execute
    pyautogui.press('enter')
    time.sleep(1)
    
    # Capture result
    region = (tp.left, tp.top, tp.width, tp.height)
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/textport_params.png', region=region)
    print('Executed and captured')
else:
    print('Textport not found')
