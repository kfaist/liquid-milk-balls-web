import pyautogui
import pygetwindow as gw
import time

print("="*70)
print("ACTIVE VERIFICATION - CHECKING TOUCHDESIGNER AND BROWSER")
print("="*70)

# Step 1: Find and focus TouchDesigner
print("\n[STEP 1] Activating TouchDesigner...")
print("-"*70)

td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    td = td_windows[0]
    print(f"[FOUND] {td.title}")
    
    # Click on TouchDesigner window to activate
    try:
        # Move to center of TD window and click
        center_x = td.left + (td.width // 2)
        center_y = td.top + (td.height // 2)
        
        pyautogui.click(center_x, center_y)
        time.sleep(1)
        print("[OK] TouchDesigner activated")
        
        # Take screenshot of TouchDesigner
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save('active_check_1_touchdesigner.png')
        print("[SCREENSHOT] active_check_1_touchdesigner.png saved")
        
    except Exception as e:
        print(f"[ERROR] Could not activate TD: {e}")
else:
    print("[ERROR] TouchDesigner not found!")

# Step 2: Switch to Firefox and check console
print("\n[STEP 2] Checking Firefox Console...")
print("-"*70)

time.sleep(2)

# Find Firefox
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title or 'Mozilla' in w.title]
if firefox_windows:
    ff = firefox_windows[0]
    print(f"[FOUND] {ff.title}")
    
    try:
        # Click on Firefox to activate
        center_x = ff.left + (ff.width // 2)
        center_y = ff.top + (ff.height // 2)
        
        pyautogui.click(center_x, center_y)
        time.sleep(1)
        print("[OK] Firefox activated")
        
        # Press F12 to toggle console (in case it's not open)
        print("[ACTION] Opening Developer Console (F12)...")
        pyautogui.press('f12')
        time.sleep(2)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save('active_check_2_firefox.png')
        print("[SCREENSHOT] active_check_2_firefox.png saved")
        
    except Exception as e:
        print(f"[ERROR] Could not check Firefox: {e}")
else:
    print("[ERROR] Firefox not found!")

# Step 3: Back to TouchDesigner for final check
print("\n[STEP 3] Final TouchDesigner Check...")
print("-"*70)

time.sleep(2)

if td_windows:
    try:
        # Click TD again
        center_x = td.left + (td.width // 2)
        center_y = td.top + (td.height // 2)
        pyautogui.click(center_x, center_y)
        time.sleep(1)
        
        # Take another screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save('active_check_3_td_final.png')
        print("[SCREENSHOT] active_check_3_td_final.png saved")
        
    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "="*70)
print("ACTIVE VERIFICATION COMPLETE")
print("="*70)
print("\nScreenshots captured:")
print("  1. active_check_1_touchdesigner.png")
print("  2. active_check_2_firefox.png")
print("  3. active_check_3_td_final.png")
print("\n[ACTION NEEDED] Review screenshots to confirm:")
print("  - Video in TouchDesigner webrender operator")
print("  - Browser console connection messages")
print("="*70)
