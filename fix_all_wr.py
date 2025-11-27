import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# The correct URL for auto-connecting viewer
correct_url = "https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-input-viewer.html"

cmd = f"""# Fix all webrender nodes to use td-input-viewer.html
for n in root.findChildren(depth=5):
    if 'webrender' in n.name.lower() and hasattr(n.par, 'url'):
        old_url = n.par.url.val
        n.par.url = '{correct_url}'
        n.par.mediastream = True
        n.par.reload.pulse()
        print(f'Fixed {{n.name}}: {{old_url[:50]}}... -> td-input-viewer.html')
print('Done! All webrender nodes updated.')"""

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
    
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/url_fix_result.png')
    print('Done')
