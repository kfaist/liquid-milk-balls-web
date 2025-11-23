import pyautogui
import time
import pyperclip

def focus_and_check_td():
    """Simple check of TouchDesigner WebRTC/LiveKit setup"""
    
    print("Checking TouchDesigner setup...")
    
    # Take initial screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('td_initial_state.png')
    print("Initial screenshot saved")
    
    # Click on TouchDesigner window (assuming it's visible)
    # Try to click in the center of the screen to activate TD
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(1)
    
    # Open textport with Alt+T
    print("Opening textport...")
    pyautogui.hotkey('alt', 't')
    time.sleep(2)
    
    # Simple check command
    check_command = "print('Checking nodes...'); print([op.path for op in root.findChildren(depth=5) if 'ndi' in op.name.lower() or 'web' in op.name.lower()])"
    
    # Type the command
    pyautogui.typewrite(check_command)
    time.sleep(1)
    
    # Execute with Ctrl+Enter
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(2)
    
    # Take screenshot of textport
    screenshot2 = pyautogui.screenshot()
    screenshot2.save('td_textport_result.png')
    print("Textport screenshot saved")
    
    # Close textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Take final screenshot
    screenshot3 = pyautogui.screenshot()
    screenshot3.save('td_final_state.png')
    print("Final screenshot saved")
    
    print("\nCheck complete! Review the screenshots:")
    print("  - td_initial_state.png")
    print("  - td_textport_result.png")  
    print("  - td_final_state.png")

if __name__ == "__main__":
    focus_and_check_td()
