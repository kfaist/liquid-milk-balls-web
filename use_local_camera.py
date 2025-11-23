"""
ALTERNATIVE: Use local camera in TouchDesigner
This tests your complete OUTPUT pipeline
"""
import pyautogui
import time

print("=" * 80)
print("ALTERNATIVE SOLUTION - LOCAL CAMERA TEST")
print("=" * 80)
print("\nThis will:")
print("1. Add a Video Device In TOP (local webcam)")
print("2. Connect it to your processing chain")
print("3. Test complete OUTPUT pipeline")
print("4. Prove everything works end-to-end")
print("")
print("Then we can troubleshoot remote camera input separately")
print("=" * 80)

input("\nPress Enter when ready to continue...")

print("\nStep 1: Focusing TouchDesigner...")
time.sleep(2)

print("\nStep 2: Opening Textport...")
pyautogui.hotkey('alt', 't')
time.sleep(2)

# Clear
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

print("\nStep 3: Creating Video Device In TOP...")
cmd = """
# Create local camera input
videoin = op('/').create(videodeviceinTOP, 'local_camera')
videoin.par.device = 0
print('Created local camera:', videoin)
print('Camera active:', videoin.par.active)
print('Camera dimensions:', videoin.width, 'x', videoin.height)
"""

# Type without newlines
cmd_oneline = cmd.replace('\n', '; ')
pyautogui.write(cmd_oneline, interval=0.003)
time.sleep(0.3)
pyautogui.press('enter')
time.sleep(3)

print("\n" + "=" * 80)
print("LOCAL CAMERA CREATED!")
print("=" * 80)
print("\nIn TouchDesigner network:")
print("1. You should see 'local_camera' operator")
print("2. It should show your webcam feed")
print("3. Wire it to your processing chain")
print("4. Output goes to ndiout_livekit2 (already working)")
print("")
print("Then test:")
print("→ Open: http://localhost:3000/return-viewer.html")
print("→ Should see processed video!")
print("")
print("=" * 80)
