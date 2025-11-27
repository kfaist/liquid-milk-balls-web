import pyautogui
import pyperclip
import pygetwindow as gw
import ctypes
import time

# Restore textport and run a check command
tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    ctypes.windll.user32.ShowWindow(tp[0]._hWnd, 9)
    time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(tp[0]._hWnd)
    time.sleep(0.5)

# Check webrender status
cmd = """wr = op('/webrender1')
if wr:
    print('URL:', wr.par.url.val)
    print('Active:', wr.par.active.val)
    print('MediaStream:', wr.par.mediastream.val)
    print('Resolution:', wr.width, 'x', wr.height)
else:
    print('webrender1 not found!')
    # Try to find any webrender
    for n in root.findChildren(depth=3):
        if 'webrender' in n.name.lower():
            print('Found:', n.path)"""

pyperclip.copy(cmd)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.2)
pyautogui.press('enter')
time.sleep(1.5)

# Screenshot
region = (tp[0].left, tp[0].top, min(tp[0].width, 1200), min(tp[0].height, 600))
if region[0] >= 0:
    pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrender_status.png', region=region)
print('Done')
