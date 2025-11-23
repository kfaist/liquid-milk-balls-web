"""
Automatically configure TouchDesigner WebRender via GUI automation
"""

import time
import subprocess
import sys

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip", "--break-system-packages"], 
                  check=True, capture_output=True)
    import pyautogui
    import pyperclip

# Configuration script to run in TouchDesigner
TD_SCRIPT = """
# WebRender Configuration
ROOM = "claymation-live"
SERVER = "wss://claymation-transcription-l6e51sws.livekit.cloud"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJzdWIiOiJ0b3VjaGRlc2lnbmVyLXJlY2VpdmVyIiwiaWF0IjoxNzYzODAxODQ5LCJuYmYiOjE3NjM4MDE4NDksImV4cCI6MTc2Mzg4ODI0OX0.7r4VZzzAnbh-On6cw1D2r2kCN84K4QCcorE5-1ZyoA0"

# Find webrender operators
ops = op('/').findChildren(type=webRenderTOP, depth=10)
if not ops:
    print("No WebRender found. Creating one...")
    w = op('/').create(webRenderTOP, 'webrender_livekit_input')
    ops = [w]

# Configure each
for w in ops:
    print(f"Configuring {w.path}")
    if hasattr(w.par, 'roomname'): w.par.roomname = ROOM
    if hasattr(w.par, 'room'): w.par.room = ROOM  
    if hasattr(w.par, 'serverurl'): w.par.serverurl = SERVER
    if hasattr(w.par, 'server'): w.par.server = SERVER
    if hasattr(w.par, 'url'): w.par.url = SERVER
    if hasattr(w.par, 'token'): w.par.token = TOKEN
    if hasattr(w.par, 'accesstoken'): w.par.accesstoken = TOKEN
    if hasattr(w.par, 'active'): w.par.active = True
    print(f"Configured: {w.path}")

print("DONE! Check webrender operator for camera feed")
"""

def focus_touchdesigner():
    """Bring TouchDesigner window to focus"""
    print("Focusing TouchDesigner window...")
    
    # Find TouchDesigner window
    import win32gui
    import win32con
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "TouchDesigner" in title:
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        hwnd = windows[0][0]
        print(f"Found TouchDesigner: {windows[0][1]}")
        
        # Bring to front
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        return True
    else:
        print("TouchDesigner window not found!")
        return False

def configure_via_textport():
    """Use Textport to configure webrender"""
    print("="*60)
    print("TOUCHDESIGNER AUTO-CONFIGURATION")
    print("="*60)
    
    # Focus TouchDesigner
    if not focus_touchdesigner():
        print("ERROR: Cannot focus TouchDesigner. Make sure it's open!")
        return False
    
    print("\nOpening Textport...")
    # Alt+T opens Textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    print("Clearing Textport...")
    # Ctrl+A to select all
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.5)
    
    print("Pasting configuration script...")
    # Copy script to clipboard and paste
    pyperclip.copy(TD_SCRIPT)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    print("Executing script...")
    # Ctrl+Enter to execute
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(2)
    
    print("\n" + "="*60)
    print("CONFIGURATION SENT TO TOUCHDESIGNER")
    print("="*60)
    print("\nCheck the Textport window for results")
    print("The webrender operator should now be configured")
    print("\nNext steps:")
    print("1. Open publisher.html on your phone")
    print("2. Click 'Start Camera'")
    print("3. Check webrender operator in TouchDesigner")
    print("4. You should see your phone's camera!")
    
    return True

if __name__ == "__main__":
    try:
        configure_via_textport()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to close...")
