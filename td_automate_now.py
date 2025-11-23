"""
TouchDesigner Automation - Full Control
This will automatically configure TouchDesigner
"""
import pyautogui
import pyperclip
import time
import win32gui
import win32con

# Configuration command for TouchDesigner
TD_COMMAND = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())"

def find_touchdesigner_window():
    """Find TouchDesigner window"""
    windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "TouchDesigner" in window_text:
                windows.append((hwnd, window_text))
        return True
    win32gui.EnumWindows(callback, None)
    return windows[0] if windows else None

def configure_touchdesigner():
    """Automatically configure TouchDesigner"""
    print("=" * 70)
    print("TOUCHDESIGNER AUTOMATION - FULL CONTROL MODE")
    print("=" * 70)
    
    # Find TouchDesigner window
    print("\n1. Finding TouchDesigner window...")
    td_window = find_touchdesigner_window()
    
    if not td_window:
        print("ERROR: TouchDesigner window not found!")
        print("Make sure TouchDesigner is running.")
        return False
    
    hwnd, title = td_window
    print(f"   Found: {title}")
    
    # Bring TouchDesigner to front
    print("\n2. Bringing TouchDesigner to foreground...")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # Open Textport (Alt+T)
    print("\n3. Opening Textport (Alt+T)...")
    pyautogui.hotkey('alt', 't')
    time.sleep(1.5)
    
    # Copy command to clipboard
    print("\n4. Copying configuration command to clipboard...")
    pyperclip.copy(TD_COMMAND)
    time.sleep(0.5)
    
    # Paste command
    print("\n5. Pasting command into Textport...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    
    # Execute command
    print("\n6. Executing command (ENTER)...")
    pyautogui.press('enter')
    time.sleep(2)
    
    print("\n" + "=" * 70)
    print("CONFIGURATION COMMAND EXECUTED!")
    print("=" * 70)
    print("\nThe configuration script should now be running in TouchDesigner.")
    print("Check the Textport output to see if it worked!")
    print("\nNext steps:")
    print("1. Look at TouchDesigner Textport for results")
    print("2. Find the Web Render TOP that was created/configured")
    print("3. Test with publisher.html")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = configure_touchdesigner()
        if not success:
            print("\nAutomation failed. Please manually paste this command:")
            print(f"\n{TD_COMMAND}\n")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease manually paste this command in TD Textport:")
        print(f"\n{TD_COMMAND}\n")
