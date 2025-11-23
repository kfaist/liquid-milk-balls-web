"""
Diagnose webrender1 - Check what URL it has and status
"""
import pyautogui
import time

print("DIAGNOSING WEBRENDER1")
print("=" * 80)

# Click on TouchDesigner to ensure focus
print("Step 1: Focusing TouchDesigner (click on it now)...")
time.sleep(2)

# Open Textport
print("\nStep 2: Opening Textport...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Clear
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

# Check webrender1 status
print("\nStep 3: Checking webrender1 status...")
cmd = "wr=op('/webrender1');print('Active:',wr.par.active);print('URL:',wr.par.url);print('Dimensions:',wr.width,'x',wr.height);print('Cook:',wr.cook);print('Valid:',wr.valid)"

pyautogui.write(cmd, interval=0.003)
time.sleep(0.3)
pyautogui.press('enter')
time.sleep(2)

print("\nStep 4: Trying to reload the page...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)

cmd2 = "wr=op('/webrender1');wr.par.reload.pulse();import time;time.sleep(3);print('After reload:',wr.width,'x',wr.height)"
pyautogui.write(cmd2, interval=0.003)
time.sleep(0.3)
pyautogui.press('enter')
time.sleep(5)

print("\n" + "=" * 80)
print("Check TouchDesigner Textport for diagnostic output!")
print("=" * 80)
