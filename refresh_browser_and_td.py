import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False

print("="*70)
print("REFRESHING BROWSER - TD AUTO VIEWER")
print("="*70)

# Find Firefox
firefox_windows = [w for w in gw.getAllWindows() if 'Firefox' in w.title]
if firefox_windows:
    ff = firefox_windows[0]
    print(f"[FOUND] Firefox: {ff.title}")
    
    # Click Firefox
    ff_x = ff.left + ff.width // 2
    ff_y = ff.top + ff.height // 2
    pyautogui.click(ff_x, ff_y)
    time.sleep(0.5)
    print("[OK] Firefox activated")
    
    # Try to find td-auto-viewer tab
    # Press Ctrl+1 through Ctrl+9 to cycle tabs
    print("\n[ACTION] Looking for td-auto-viewer tab...")
    
    # Open new tab with td-auto-viewer
    print("[ACTION] Opening fresh td-auto-viewer tab...")
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
    
    # Type URL
    url = "localhost:3000/td-auto-viewer.html"
    pyautogui.write(url, interval=0.02)
    pyautogui.press('enter')
    time.sleep(3)
    
    print("[OK] Fresh td-auto-viewer page loaded")
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('browser_td_viewer_fresh.png')
    print("[SCREENSHOT] browser_td_viewer_fresh.png")
    
    # Now go back to TouchDesigner and reload again
    print("\n[ACTION] Switching back to TouchDesigner...")
    td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
    if td_windows:
        td = td_windows[0]
        td_x = td.left + td.width // 2
        td_y = td.top + td.height // 2
        pyautogui.click(td_x, td_y)
        time.sleep(1)
        
        # Open textport
        pyautogui.hotkey('alt', 't')
        time.sleep(1)
        
        # Reload webrender
        cmd = "op('/webrender_livekit_input').par.reload.pulse()"
        pyautogui.write(cmd, interval=0.01)
        pyautogui.press('enter')
        time.sleep(2)
        
        print("[OK] Webrender reloaded after browser refresh")
        
        # Take final screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save('td_after_browser_refresh.png')
        print("[SCREENSHOT] td_after_browser_refresh.png")
    
    print("\n" + "="*70)
    print("BROWSER REFRESH COMPLETE!")
    print("="*70)
    print("\nActions taken:")
    print("1. Opened fresh td-auto-viewer page in browser")
    print("2. Reloaded TouchDesigner webrender")
    print("\nCheck TouchDesigner webrender_livekit_input now!")
    print("="*70)
    
else:
    print("[ERROR] Firefox not found!")
