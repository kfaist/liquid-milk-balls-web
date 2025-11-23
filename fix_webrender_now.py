import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False

print("="*70)
print("TROUBLESHOOTING TOUCHDESIGNER WEBRENDER - FIXING NOW!")
print("="*70)

# Step 1: Activate TouchDesigner
print("\n[STEP 1] Activating TouchDesigner...")
td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
if td_windows:
    td = td_windows[0]
    td_x = td.left + td.width // 2
    td_y = td.top + td.height // 2
    pyautogui.click(td_x, td_y)
    time.sleep(1)
    print("[OK] TouchDesigner activated")
    
    # Step 2: Open Textport
    print("\n[STEP 2] Opening Textport (Alt+T)...")
    pyautogui.hotkey('alt', 't')
    time.sleep(1.5)
    print("[OK] Textport should be open")
    
    # Step 3: Set webrender URL
    print("\n[STEP 3] Setting webrender URL...")
    cmd1 = "op('/webrender_livekit_input').par.url = 'http://localhost:3000/td-auto-viewer.html'"
    pyautogui.write(cmd1, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.5)
    print("[OK] URL set")
    
    # Step 4: Activate webrender
    print("\n[STEP 4] Activating webrender...")
    cmd2 = "op('/webrender_livekit_input').par.active = True"
    pyautogui.write(cmd2, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.5)
    print("[OK] Webrender activated")
    
    # Step 5: Reload webrender
    print("\n[STEP 5] Reloading webrender...")
    cmd3 = "op('/webrender_livekit_input').par.reload.pulse()"
    pyautogui.write(cmd3, interval=0.01)
    pyautogui.press('enter')
    time.sleep(2)
    print("[OK] Reload pulsed")
    
    # Step 6: Check resolution
    print("\n[STEP 6] Setting resolution...")
    cmd4 = "op('/webrender_livekit_input').par.width = 1280"
    pyautogui.write(cmd4, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.3)
    
    cmd5 = "op('/webrender_livekit_input').par.height = 720"
    pyautogui.write(cmd5, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.5)
    print("[OK] Resolution set to 1280x720")
    
    # Step 7: One more reload
    print("\n[STEP 7] Final reload...")
    cmd6 = "op('/webrender_livekit_input').par.reload.pulse()"
    pyautogui.write(cmd6, interval=0.01)
    pyautogui.press('enter')
    time.sleep(2)
    print("[OK] Final reload complete")
    
    # Take screenshot
    print("\n[STEP 8] Taking screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save('td_after_fix.png')
    print("[OK] Screenshot saved: td_after_fix.png")
    
    print("\n" + "="*70)
    print("TROUBLESHOOTING COMPLETE!")
    print("="*70)
    print("\nCommands executed:")
    print("1. Set URL to localhost:3000/td-auto-viewer.html")
    print("2. Activated webrender")
    print("3. Reloaded webrender (twice)")
    print("4. Set resolution to 1280x720")
    print("\nCheck TouchDesigner now - webrender should show video!")
    print("="*70)
    
else:
    print("[ERROR] TouchDesigner not found!")
