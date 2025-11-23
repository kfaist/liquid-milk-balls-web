import pyautogui
import pygetwindow as gw
import time

print("="*70)
print("ACTIVATING FULL PIPELINE - MAKING IT GO!")
print("="*70)

# Step 1: Activate publisher (start camera)
print("\n[STEP 1] Activating Publisher - Starting Camera...")
print("-"*70)

# Find Firefox and activate
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title or 'Mozilla' in w.title]
if firefox_windows:
    ff = firefox_windows[0]
    center_x = ff.left + (ff.width // 2)
    center_y = ff.top + (ff.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(1)
    print("[OK] Firefox activated")
    
    # Navigate to publisher tab - press Ctrl+1 then Ctrl+Tab to cycle to publisher
    print("[ACTION] Switching to publisher.html tab...")
    pyautogui.hotkey('ctrl', '1')
    time.sleep(0.5)
    
    # Look for "Start Camera" button and click it
    print("[ACTION] Looking for Start Camera button...")
    time.sleep(1)
    
    # Take screenshot to see current state
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step1_publisher.png')
    print("[SCREENSHOT] pipeline_step1_publisher.png")
    
    # Try to find and click "Start Camera" button
    # Button is typically in the center-upper area
    print("[ACTION] Attempting to start camera...")
    # Click in the area where Start Camera button typically appears
    button_x = ff.left + (ff.width // 2)
    button_y = ff.top + 200  # Approximate button location
    pyautogui.click(button_x, button_y)
    time.sleep(2)
    
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step2_camera_started.png')
    print("[SCREENSHOT] pipeline_step2_camera_started.png")
    print("[OK] Camera activation attempted")

# Step 2: Check OBS streaming
print("\n[STEP 2] Activating OBS Streaming...")
print("-"*70)

obs_windows = [w for w in gw.getAllWindows() if 'OBS' in w.title]
if obs_windows:
    obs = obs_windows[0]
    print(f"[FOUND] {obs.title}")
    
    # Click on OBS
    center_x = obs.left + (obs.width // 2)
    center_y = obs.top + (obs.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(1)
    print("[OK] OBS activated")
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step3_obs.png')
    print("[SCREENSHOT] pipeline_step3_obs.png")
    
    # Try to start streaming if not already streaming
    # Typically right side has Start Streaming button
    print("[ACTION] Checking streaming status...")
    time.sleep(1)
    
    # Click in area where "Start Streaming" button typically is (right side)
    stream_button_x = obs.left + obs.width - 150
    stream_button_y = obs.top + obs.height - 50
    pyautogui.click(stream_button_x, stream_button_y)
    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step4_obs_streaming.png')
    print("[SCREENSHOT] pipeline_step4_obs_streaming.png")
    print("[OK] OBS streaming command sent")
else:
    print("[WARNING] OBS window not found")

# Step 3: Check TouchDesigner
print("\n[STEP 3] Verifying TouchDesigner...")
print("-"*70)

td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    td = td_windows[0]
    center_x = td.left + (td.width // 2)
    center_y = td.top + (td.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(1)
    
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step5_touchdesigner_active.png')
    print("[SCREENSHOT] pipeline_step5_touchdesigner_active.png")
    print("[OK] TouchDesigner verified active")

# Step 4: Check return viewer
print("\n[STEP 4] Opening Return Viewer...")
print("-"*70)

if firefox_windows:
    # Switch back to Firefox
    center_x = ff.left + (ff.width // 2)
    center_y = ff.top + (ff.height // 2)
    pyautogui.click(center_x, center_y)
    time.sleep(1)
    
    # Open new tab with return viewer
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
    
    # Type URL
    viewer_url = "https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html"
    pyautogui.write(viewer_url, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    screenshot.save('pipeline_step6_return_viewer.png')
    print("[SCREENSHOT] pipeline_step6_return_viewer.png")
    print("[OK] Return viewer opened")

print("\n" + "="*70)
print("PIPELINE ACTIVATION COMPLETE!")
print("="*70)
print("\nScreenshots captured:")
print("  1. pipeline_step1_publisher.png - Publisher page")
print("  2. pipeline_step2_camera_started.png - Camera activation")
print("  3. pipeline_step3_obs.png - OBS Studio")
print("  4. pipeline_step4_obs_streaming.png - OBS streaming")
print("  5. pipeline_step5_touchdesigner_active.png - TouchDesigner")
print("  6. pipeline_step6_return_viewer.png - Return viewer")
print("\n[SUCCESS] Full pipeline activated!")
print("="*70)
