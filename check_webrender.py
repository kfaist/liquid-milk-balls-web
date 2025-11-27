import pyautogui
import pygetwindow as gw
import time

# Minimize textport
tp = [w for w in gw.getAllWindows() if 'Textport' in w.title]
if tp:
    tp[0].minimize()
    time.sleep(0.3)

# Take screenshot
pyautogui.screenshot('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_webrender_after_fix.png', region=(100, 50, 1600, 900))
print('Done')
