"""
Direct approach - Type into TouchDesigner Textport
"""
import pyautogui
import time

print("CONFIGURING WEBRENDER1 - DIRECT APPROACH")
print("=" * 80)

# Give user time to click on TouchDesigner window
print("\nStep 1: Click on TouchDesigner window NOW...")
print("You have 3 seconds...")
time.sleep(3)

print("\nStep 2: Opening Textport...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

print("\nStep 3: Sending configuration command...")
# Clear
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

# Type command
cmd = "wr=op('/webrender1');wr.par.active=0;import time;time.sleep(0.5);wr.par.active=1;wr.par.url='http://localhost:3000/td-auto-viewer.html';wr.par.reload.pulse();time.sleep(5);print('Result:',wr.width,'x',wr.height)"

print(f"Typing: {cmd[:50]}...")
pyautogui.write(cmd, interval=0.002)
time.sleep(0.5)

print("\nStep 4: Executing (pressing Enter)...")
pyautogui.press('enter')

print("\nWaiting 10 seconds for configuration to complete...")
time.sleep(10)

print("\n" + "=" * 80)
print("DONE! Check TouchDesigner Textport for output.")
print("Should show: Result: [width] x [height]")
print("=" * 80)
