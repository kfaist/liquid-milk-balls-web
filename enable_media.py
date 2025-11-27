import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Command to enable media stream with correct parameter name
cmd = """wr.par.mediastream = True
wr.par.audio = 'on'
wr.par.reload.pulse()
print('Media stream enabled:', wr.par.mediastream.val)
print('Audio:', wr.par.audio.val)"""

# Copy to clipboard
pyperclip.copy(cmd)
print('Copied enable command to clipboard')

# Find and activate Textport window
tp_windows = [w for w in gw.getAllWindows() if w.title == 'Textport']
if tp_windows:
    tp = tp_windows[0]
    ctypes.windll.user32.SetForegroundWindow(tp._hWnd)
    time.sleep(0.5)
    
    # Paste
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # Press Enter to execute each line
    pyautogui.press('enter')
    time.sleep(1.5)
    
    # Capture result
    region = (tp.left, tp.top, tp.width, tp.height)
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/textport_enabled.png', region=region)
    print('Done')
else:
    print('Textport not found')
