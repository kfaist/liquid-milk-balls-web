#!/usr/bin/env python3
"""
Check Firefox Browser Consoles
Automate opening DevTools and checking for LiveKit connection messages
"""
import pyautogui
import time
import pygetwindow as gw

def find_window(title_contains):
    """Find window by partial title match"""
    windows = gw.getWindowsWithTitle(title_contains)
    return windows[0] if windows else None

def check_browser_console():
    """Open Firefox and check console"""
    print("="*60)
    print("CHECKING FIREFOX BROWSER CONSOLE")
    print("="*60)
    
    # Find Firefox window
    ff_window = find_window('Firefox')
    
    if not ff_window:
        print("[FAIL] Firefox window not found")
        return False
    
    print(f"[OK] Firefox found: {ff_window.title}")
    
    # Bring Firefox to front
    try:
        ff_window.activate()
        time.sleep(2)
        print("[OK] Firefox activated")
    except Exception as e:
        print(f"[WARN] Could not fully activate: {e}")
        # Continue anyway
    
    # Open new tab to navigate to td-auto-viewer
    print("[ACTION] Opening td-auto-viewer.html...")
    pyautogui.hotkey('ctrl', 't')  # New tab
    time.sleep(1)
    
    # Type the URL
    pyautogui.write('localhost:3000/td-auto-viewer.html', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3)  # Wait for page to load
    
    print("[OK] Navigated to td-auto-viewer.html")
    
    # Open Developer Console (F12)
    print("[ACTION] Opening Developer Console...")
    pyautogui.press('f12')
    time.sleep(2)
    
    # Switch to Console tab (Ctrl+Shift+K on Firefox)
    print("[ACTION] Switching to Console tab...")
    pyautogui.hotkey('ctrl', 'shift', 'k')
    time.sleep(1)
    
    # Take screenshot of console
    print("[ACTION] Capturing console screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save('console_td_viewer.png')
    print("[OK] Console screenshot saved: console_td_viewer.png")
    
    print("\n" + "="*60)
    print("NEXT: Check publisher.html")
    print("="*60)
    
    # Open new tab for publisher
    print("[ACTION] Opening publisher.html...")
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
    
    pyautogui.write('localhost:3000/publisher.html', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3)
    
    print("[OK] Navigated to publisher.html")
    
    # Open console for publisher
    print("[ACTION] Opening console for publisher...")
    pyautogui.press('f12')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'shift', 'k')
    time.sleep(1)
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('console_publisher.png')
    print("[OK] Publisher console screenshot saved: console_publisher.png")
    
    print("\n" + "="*60)
    print("CONSOLE CHECK COMPLETE")
    print("="*60)
    print("\nScreenshots saved:")
    print("  - console_td_viewer.png (td-auto-viewer.html console)")
    print("  - console_publisher.png (publisher.html console)")
    print("\nLook for:")
    print("  [TD-VIEWER] Connected: claymation-live")
    print("  [PUBLISHER] Camera started")
    print("  [PUBLISHER] Publishing to claymation-live")
    
    return True

def main():
    try:
        check_browser_console()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
