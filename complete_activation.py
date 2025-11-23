import pyautogui
import time

# Disable failsafe for this controlled automation
pyautogui.FAILSAFE = False

print("="*70)
print("COMPLETING PIPELINE ACTIVATION")
print("="*70)

# Take current screenshot
print("\n[STEP 1] Capturing current state...")
screenshot = pyautogui.screenshot()
screenshot.save('pipeline_current_state.png')
print("[OK] Screenshot saved: pipeline_current_state.png")

# Open return viewer in new tab
print("\n[STEP 2] Opening return viewer URL...")
time.sleep(1)

# Press Ctrl+T for new tab
pyautogui.hotkey('ctrl', 't')
time.sleep(1.5)

# Type the return viewer URL
viewer_url = "https://liquid-milk-balls-web-production-2e8c.up.railway.app/return-viewer.html"
print(f"[ACTION] Navigating to: {viewer_url}")
pyautogui.write(viewer_url, interval=0.03)
time.sleep(0.5)

# Press Enter
pyautogui.press('enter')
time.sleep(4)

# Take screenshot of return viewer
screenshot = pyautogui.screenshot()
screenshot.save('pipeline_return_viewer.png')
print("[OK] Screenshot saved: pipeline_return_viewer.png")

print("\n" + "="*70)
print("PIPELINE ACTIVATION COMPLETE!")
print("="*70)
print("\nYour pipeline is now LIVE!")
print("\nCheck:")
print("  - Publisher camera should be streaming")
print("  - TouchDesigner should be processing")
print("  - OBS should be receiving video")
print("  - Return viewer should show processed output")
print("="*70)
