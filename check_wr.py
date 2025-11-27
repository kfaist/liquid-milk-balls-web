import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Open textport
td = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td:
    ctypes.windll.user32.SetForegroundWindow(td[0]._hWnd)
    time.sleep(0.3)
    
    # Alt+T to open textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Check webrender status
    cmd = """wr = op('/webrender1')
if wr:
    print('URL:', wr.par.url.val)
    print('Resolution:', wr.width, 'x', wr.height)
    print('Active:', wr.par.active.val)
else:
    print('webrender1 not found - searching...')
    for n in root.findChildren(depth=5):
        if 'webrender' in n.name.lower():
            print('Found:', n.path, n.width, 'x', n.height)"""
    
    pyperclip.copy(cmd)
    time.sleep(0.3)
    
    # Find textport and paste
    tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
    if tp:
        ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(1)
        
        # Screenshot
        pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/wr_status.png')
        print('Done')
