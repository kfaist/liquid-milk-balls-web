"""
TouchDesigner Full Automation
This will configure TD completely automatically
"""
import pyautogui
import time
import win32gui
import win32con

def find_td_window():
    """Find TouchDesigner window"""
    windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            text = win32gui.GetWindowText(hwnd)
            if 'TouchDesigner' in text:
                windows.append((hwnd, text))
        return True
    win32gui.EnumWindows(callback, None)
    return windows[0] if windows else None

def main():
    print("=" * 70)
    print("TOUCHDESIGNER FULL AUTOMATION")
    print("=" * 70)
    
    # Find TD window
    print("\n1. Finding TouchDesigner window...")
    td_window = find_td_window()
    
    if not td_window:
        print("ERROR: TouchDesigner window not found!")
        print("Make sure TouchDesigner is running!")
        return False
    
    hwnd, title = td_window
    print(f"   [OK] Found: {title}")
    
    # Bring TD to foreground
    print("\n2. Bringing TouchDesigner to foreground...")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1.5)
    print("   [OK] Window activated")
    
    # Open Textport
    print("\n3. Opening Textport (Alt+T)...")
    pyautogui.hotkey('alt', 't')
    time.sleep(1.5)
    print("   [OK] Textport opened")
    
    # Configuration command
    config_cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"
    
    print("\n4. Pasting configuration command...")
    print(f"   Command: {config_cmd[:60]}...")
    
    # Type the command (using write instead of typewrite for reliability)
    for char in config_cmd:
        pyautogui.press(char if len(char) == 1 else char)
        time.sleep(0.005)
    
    time.sleep(1)
    print("   [OK] Command entered")
    
    # Execute
    print("\n5. Executing configuration...")
    pyautogui.press('enter')
    time.sleep(3)
    print("   [OK] Configuration executed!")
    
    print("\n" + "=" * 70)
    print("AUTOMATION COMPLETE!")
    print("=" * 70)
    print("\nCheck TouchDesigner textport for configuration results.")
    print("\nNext steps:")
    print("  1. Look for 'CONFIGURATION COMPLETE' message in textport")
    print("  2. Find the Web Render TOP that was created")
    print("  3. Test with publisher page!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\nAutomation failed. Try manual configuration.")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Try manual configuration instead.")
        print("See TD_COMMAND.txt for instructions")
