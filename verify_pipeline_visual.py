import pyautogui
import pygetwindow as gw
import time

print("="*60)
print("TOUCHDESIGNER WEBRTC PIPELINE VERIFICATION")
print("="*60)

# Step 1: Check TouchDesigner
print("\n[STEP 1] Checking TouchDesigner...")
print("-" * 60)

td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    print("[OK] TouchDesigner found: " + td_windows[0].title)
    
    # Try to activate TouchDesigner
    try:
        # Use Alt+Tab to switch to TD
        print("   Switching to TouchDesigner window...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        
        # Try multiple times if needed
        for i in range(5):
            try:
                current_title = pyautogui.getActiveWindow()
                if current_title and 'TouchDesigner' in current_title.title:
                    print("   [OK] TouchDesigner is now active")
                    break
            except:
                pass
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
        
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save('verification_1_touchdesigner.png')
        print("   [SCREENSHOT] Saved: verification_1_touchdesigner.png")
        print("   [CHECK] Look at webrender_livekit_input operator for video")
        
    except Exception as e:
        print("   [WARNING] Could not activate TD window: " + str(e))
else:
    print("[ERROR] TouchDesigner window not found!")

# Step 2: Check Browser - td-auto-viewer.html
print("\n[STEP 2] Checking Browser Console...")
print("-" * 60)

firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title or 'Mozilla' in w.title]
if firefox_windows:
    print("[OK] Firefox found: " + firefox_windows[0].title)
    
    try:
        # Switch to Firefox
        print("   Switching to Firefox...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        
        for i in range(5):
            try:
                current_title = pyautogui.getActiveWindow()
                if current_title and ('Firefox' in current_title.title or 'Mozilla' in current_title.title):
                    print("   [OK] Firefox is now active")
                    break
            except:
                pass
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
        
        time.sleep(1)
        
        # Open Developer Console
        print("   Opening Developer Console (F12)...")
        pyautogui.press('f12')
        time.sleep(2)
        
        screenshot = pyautogui.screenshot()
        screenshot.save('verification_2_browser_console.png')
        print("   [SCREENSHOT] Saved: verification_2_browser_console.png")
        print("   [CHECK] Look for '[TD-VIEWER] Connected' messages")
        
    except Exception as e:
        print("   [WARNING] Could not check browser: " + str(e))
else:
    print("[ERROR] Firefox window not found!")

# Step 3: Summary
print("\n" + "="*60)
print("VERIFICATION SCREENSHOTS CAPTURED")
print("="*60)
print("\nReview these screenshots:")
print("   1. verification_1_touchdesigner.png")
print("      -> Check webrender_livekit_input operator for video")
print("\n   2. verification_2_browser_console.png")
print("      -> Look for '[TD-VIEWER] Connected: claymation-live'")
print("      -> Check for video subscription messages")
print("\n" + "="*60)
print("[COMPLETE] Automated verification complete!")
print("[ACTION NEEDED] Manual review of screenshots required")
print("="*60)
