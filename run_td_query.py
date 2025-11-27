import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# The command to paste
cmd = """wr = op('/webrender_livekit_input')
for p in wr.pars():
    if 'media' in p.name.lower() or 'audio' in p.name.lower():
        print(f"{p.name} = {p.val}")"""

# Copy to clipboard
pyperclip.copy(cmd)
print('Copied command to clipboard')

# Find and activate TouchDesigner
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    ctypes.windll.user32.SetForegroundWindow(td_windows[0]._hWnd)
    time.sleep(0.5)
    
    # Paste into textport
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Press Enter to execute
    pyautogui.press('enter')
    time.sleep(1)
    
    # Take screenshot to see result
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_param_result.png')
    print('Pasted and executed command')
else:
    print('TD not found')
