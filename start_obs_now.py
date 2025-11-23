import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False

print("STARTING OBS STREAM...")

# Find OBS window
obs_windows = [w for w in gw.getAllWindows() if 'OBS' in w.title]
if obs_windows:
    obs = obs_windows[0]
    print(f"Found OBS: {obs.title}")
    
    # Click on OBS to activate
    center_x = obs.left + (obs.width // 2)
    center_y = obs.top + (obs.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)
    
    # Look for Start Streaming button - typically bottom right
    # Try clicking in the bottom right area where controls are
    controls_x = obs.left + obs.width - 120
    controls_y = obs.top + obs.height - 40
    
    print("Clicking Start Streaming area...")
    pyautogui.click(controls_x, controls_y)
    time.sleep(1)
    
    print("[OK] Stream start attempted!")
else:
    print("[ERROR] OBS not found!")
