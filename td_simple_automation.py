"""
Simple TouchDesigner Automation - Using Clipboard
"""
import pyperclip
import pyautogui
import time
import win32gui

def find_td_window():
    """Find TouchDesigner window"""
    windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            text = win32gui.GetWindowText(hwnd)
            if 'TouchDesigner' in text:
                rect = win32gui.GetWindowRect(hwnd)
                windows.append((hwnd, text, rect))
        return True
    win32gui.EnumWindows(callback, None)
    return windows[0] if windows else None

def main():
    print("=" * 70)
    print("TOUCHDESIGNER AUTOMATION - CLIPBOARD METHOD")
    print("=" * 70)
    
    # Configuration command
    config_cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"
    
    print("\n1. Finding TouchDesigner window...")
    td_window = find_td_window()
    
    if not td_window:
        print("ERROR: TouchDesigner not found!")
        return False
    
    hwnd, title, rect = td_window
    print(f"   [OK] Found: {title}")
    
    # Get window center
    x = (rect[0] + rect[2]) // 2
    y = (rect[1] + rect[3]) // 2
    
    print(f"\n2. Clicking TouchDesigner window at ({x}, {y})...")
    pyautogui.click(x, y)
    time.sleep(1)
    print("   [OK] Window activated")
    
    print("\n3. Opening Textport (Alt+T)...")
    pyautogui.hotkey('alt', 't')
    time.sleep(2)
    print("   [OK] Textport should be open")
    
    print("\n4. Copying command to clipboard...")
    pyperclip.copy(config_cmd)
    print(f"   Command: {config_cmd[:60]}...")
    print("   [OK] Copied to clipboard")
    
    print("\n5. Pasting and executing...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    print("   [OK] Command executed!")
    
    print("\n" + "=" * 70)
    print("AUTOMATION COMPLETE!")
    print("=" * 70)
    print("\nCheck TouchDesigner textport for results.")
    print("Look for 'CONFIGURATION COMPLETE' message.")
    print("\nIf you see errors, try manual configuration:")
    print("  1. Open Textport (Alt+T)")
    print("  2. Paste the command (it's in your clipboard)")
    print("  3. Press Enter")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nMANUAL STEPS:")
        print("1. Click on TouchDesigner")
        print("2. Press Alt+T to open Textport")
        print("3. Paste this command (already in clipboard):")
        print("   exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())")
        print("4. Press Enter")
