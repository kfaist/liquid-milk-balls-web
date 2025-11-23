"""
Automate adding WebRender TOP to TouchDesigner for camera input
"""

import pyautogui
import time
import pyperclip

print("=" * 60)
print("SETTING UP TOUCHDESIGNER CAMERA INPUT")
print("=" * 60)

# The command to run in TouchDesigner's Textport
td_command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/setup_td_input.py').read())"

print("\n[1/4] Copying command to clipboard...")
pyperclip.copy(td_command)
print("Command copied!")

print("\n[2/4] Activating TouchDesigner window...")
time.sleep(1)

# Find and click TouchDesigner window
import pygetwindow as gw
td_windows = [w for w in gw.getAllTitles() if 'TouchDesigner' in w]

if td_windows:
    print(f"Found TouchDesigner: {td_windows[0]}")
    td_window = gw.getWindowsWithTitle(td_windows[0])[0]
    td_window.activate()
    time.sleep(1)
else:
    print("TouchDesigner window not found!")
    print("Please click on TouchDesigner window manually")
    time.sleep(3)

print("\n[3/4] Opening Textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(1.5)

print("\n[4/4] Pasting and running command...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
pyautogui.press('enter')

print("\n" + "=" * 60)
print("COMMAND SENT TO TOUCHDESIGNER!")
print("=" * 60)
print("""
Check TouchDesigner Textport for results.

The script will:
- Create webrender_livekit_input operator
- Set URL to td-auto-viewer.html  
- Configure for 1920x1080
- Open viewer window
- Show you where to connect it

After LiveKit upgrade completes:
1. Open publisher.html
2. Click 'Start Publishing'
3. WebRender TOP will show camera!
""")
