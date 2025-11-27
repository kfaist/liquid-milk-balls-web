import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Find textport
tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.5)
    
    # Simple status check
    cmd = "print('URL:', op('/webrender1').par.url.val, 'Size:', op('/webrender1').width, 'x', op('/webrender1').height)"
    pyperclip.copy(cmd)
    
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)
    
    # Screenshot
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/wr_check.png', region=(tp[0].left, tp[0].top, 1000, 500))
    print('Done')
