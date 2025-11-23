"""
TouchDesigner UI Automation Script
This will configure the Web Render TOP using UI automation
"""
import pyautogui
import time
import sys

# Configuration
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
ROOM_NAME = "claymation-live"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs"

def configure_touchdesigner():
    """
    Automate TouchDesigner configuration
    """
    print("=" * 60)
    print("TOUCHDESIGNER AUTOMATION SCRIPT")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Find TouchDesigner window")
    print("2. Create a Web Render TOP")
    print("3. Configure it for LiveKit")
    print("\n" + "=" * 60)
    
    # Wait for user to position TD window
    print("\nMAKE SURE TOUCHDESIGNER IS VISIBLE!")
    print("You have 5 seconds to click on the TD window...")
    time.sleep(5)
    
    try:
        # Try to find TouchDesigner window
        import win32gui
        
        def find_window(title_substring):
            windows = []
            def callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if title_substring.lower() in window_text.lower():
                        windows.append((hwnd, window_text))
                return True
            win32gui.EnumWindows(callback, None)
            return windows
        
        td_windows = find_window("TouchDesigner")
        
        if not td_windows:
            print("ERROR: Could not find TouchDesigner window!")
            print("Make sure TouchDesigner is running and visible.")
            return False
        
        hwnd, title = td_windows[0]
        print(f"\nFound TouchDesigner: {title}")
        
        # Bring TD to front
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        
        print("\n" + "=" * 60)
        print("CREATING WEB RENDER TOP...")
        print("=" * 60)
        
        # Press TAB to open operator menu
        print("\n1. Opening operator menu (TAB)...")
        pyautogui.press('tab')
        time.sleep(0.5)
        
        # Type to search for Web Render
        print("2. Searching for 'web render'...")
        pyautogui.write('web render', interval=0.05)
        time.sleep(0.5)
        
        # Press Enter to select
        print("3. Creating operator (ENTER)...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Click to place it
        print("4. Placing operator (click)...")
        pyautogui.click()
        time.sleep(1)
        
        print("\n✓ Web Render TOP created!")
        
        print("\n" + "=" * 60)
        print("MANUAL CONFIGURATION REQUIRED")
        print("=" * 60)
        print("\nThe Web Render TOP is now created.")
        print("You need to manually set these parameters:")
        print(f"\n  LiveKit URL: {LIVEKIT_URL}")
        print(f"  Room Name: {ROOM_NAME}")
        print(f"  Token: {TOKEN[:50]}...")
        print("\nLook for parameters like:")
        print("  - livekiturl, url, serverurl")
        print("  - roomname, room, channelname")
        print("  - token, livekittoken, accesstoken")
        print("  - uselivekit, enablelivekit (turn ON)")
        
        return True
        
    except ImportError:
        print("\nERROR: win32gui not available!")
        print("Install with: pip install pywin32")
        return False
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nYou will need to configure TD manually.")
        print("Follow the instructions in QUICK_START.txt")
        return False

if __name__ == "__main__":
    success = configure_touchdesigner()
    
    print("\n" + "=" * 60)
    if success:
        print("CONFIGURATION STARTED!")
        print("\nNext: Set the LiveKit parameters in the Web Render TOP")
    else:
        print("AUTOMATION FAILED")
        print("\nPlease configure manually using QUICK_START.txt")
    print("=" * 60)
