"""
TouchDesigner WebRTC/LiveKit Diagnostic and Fix Script
This script will help diagnose and fix the WebRTC/LiveKit nodes in your TouchDesigner project
"""

import pyautogui
import time
import subprocess
import pygetwindow as gw
import keyboard

def focus_touchdesigner():
    """Focus on TouchDesigner window"""
    print("Looking for TouchDesigner window...")
    windows = gw.getWindowsWithTitle('TouchDesigner')
    
    if windows:
        td_window = windows[0]
        td_window.activate()
        time.sleep(1)
        print(f"Found and focused: {td_window.title}")
        return True
    else:
        print("TouchDesigner window not found!")
        return False

def check_webrender_nodes():
    """Check for Web Render TOPs in the project"""
    print("\nChecking for Web Render TOPs...")
    
    # Press 'n' to open network editor if not already open
    pyautogui.press('n')
    time.sleep(0.5)
    
    # Search for webrender nodes
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite('webrender')
    time.sleep(1)
    
    # Close search
    pyautogui.press('escape')
    
    print("✓ Search for webrender nodes complete")
    return True

def create_webrtc_receiver():
    """Create a Web Render TOP for receiving WebRTC"""
    print("\nCreating WebRTC Receiver node...")
    
    # Open operator palette
    pyautogui.press('tab')
    time.sleep(0.5)
    
    # Type to search for Web Render
    pyautogui.typewrite('web render')
    time.sleep(0.5)
    
    # Select Web Render TOP
    pyautogui.press('enter')
    time.sleep(1)
    
    # Click to place it
    pyautogui.click(pyautogui.position()[0] + 100, pyautogui.position()[1])
    time.sleep(1)
    
    print("✓ Web Render TOP created")
    
    # Configure the Web Render TOP
    configure_webrender_input()
    
    return True

def configure_webrender_input():
    """Configure the Web Render TOP for LiveKit input"""
    print("\nConfiguring Web Render TOP for LiveKit...")
    
    # Open parameter window (press 'p')
    pyautogui.press('p')
    time.sleep(1)
    
    # Click on URL field (approximate position)
    # We'll need to tab through parameters
    pyautogui.press('tab')
    time.sleep(0.2)
    
    # Clear and enter URL
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite('http://localhost:3000/td-bidirectional.html')
    time.sleep(0.5)
    
    # Tab to resolution fields
    for _ in range(3):
        pyautogui.press('tab')
        time.sleep(0.2)
    
    # Set resolution
    pyautogui.typewrite('1920')
    pyautogui.press('tab')
    pyautogui.typewrite('1080')
    
    print("✓ Web Render TOP configured with LiveKit URL")
    return True

def create_ndi_output():
    """Create an NDI Out TOP for sending processed video"""
    print("\nCreating NDI Output node...")
    
    # Open operator palette
    pyautogui.press('tab')
    time.sleep(0.5)
    
    # Type to search for NDI Out
    pyautogui.typewrite('ndi out')
    time.sleep(0.5)
    
    # Select NDI Out TOP
    pyautogui.press('enter')
    time.sleep(1)
    
    # Click to place it
    pyautogui.click(pyautogui.position()[0] + 300, pyautogui.position()[1])
    time.sleep(1)
    
    print("✓ NDI Out TOP created")
    
    # Configure NDI Out
    pyautogui.press('p')
    time.sleep(1)
    
    # Set NDI name
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite('TD-Processed-Stream')
    
    print("✓ NDI Out configured")
    return True

def test_server_connection():
    """Test if the local server is running"""
    print("\nTesting server connection...")
    
    import requests
    try:
        response = requests.get('http://localhost:3000/healthz', timeout=5)
        if response.status_code == 200:
            print("✓ Server is running on http://localhost:3000")
            return True
    except:
        print("✗ Server is not running!")
        print("  Please start the server with: npm start")
        return False
    
    return False

def test_livekit_tokens():
    """Test if LiveKit tokens can be generated"""
    print("\nTesting LiveKit token generation...")
    
    import requests
    try:
        # Test publisher token
        response = requests.get('http://localhost:3000/api/publisher-token', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✓ Publisher token generation working")
                print(f"  Room: {data.get('room', 'unknown')}")
                print(f"  URL: {data.get('url', 'unknown')[:50]}...")
            else:
                print("✗ Token generation failed")
                return False
        
        # Test viewer token
        response = requests.get('http://localhost:3000/api/viewer-token', timeout=5)
        if response.status_code == 200:
            print("✓ Viewer token generation working")
            return True
            
    except Exception as e:
        print(f"✗ Error testing tokens: {e}")
        return False
    
    return False

def main():
    print("=" * 60)
    print("TouchDesigner WebRTC/LiveKit Diagnostic Tool")
    print("=" * 60)
    
    # First test server and LiveKit
    server_ok = test_server_connection()
    if server_ok:
        livekit_ok = test_livekit_tokens()
    else:
        print("\n⚠️  Please start the server first!")
        print("  Run: cd liquid-milk-balls-web && npm start")
        return
    
    # Focus TouchDesigner
    if not focus_touchdesigner():
        print("\n⚠️  Please open TouchDesigner first!")
        return
    
    print("\nDiagnostic Results:")
    print("-" * 40)
    print(f"✓ Server Running: {server_ok}")
    print(f"✓ LiveKit Configured: {livekit_ok}")
    print(f"✓ TouchDesigner Found: True")
    
    print("\n" + "=" * 60)
    print("SETUP INSTRUCTIONS:")
    print("=" * 60)
    
    print("""
1. IN TOUCHDESIGNER:
   - Create a Web Render TOP
   - Set URL: http://localhost:3000/td-bidirectional.html
   - Set Resolution: 1920 x 1080
   - Enable Audio: ON
   - Set Active: ON

2. CLICK START IN THE WEB RENDER:
   - Use mouse interaction in TouchDesigner
   - Click the START button in the rendered page
   - Status should change to "CONNECTED"

3. CONNECT YOUR PROCESSING:
   - Web Render TOP output → Your effects network
   - Your processed output → NDI Out TOP
   - NDI Name: TD-Processed-Stream

4. TEST WITH PHONE:
   - On phone browser: http://YOUR-IP:3000/publisher.html
   - Click "Start Publishing"
   - You should see the feed in TouchDesigner!

5. VIEW PROCESSED OUTPUT:
   - On phone: http://YOUR-IP:3000/return-viewer.html
   - Click "Connect"
   - You'll see your processed video!
    """)
    
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING:")
    print("=" * 60)
    
    print("""
If WebRTC nodes aren't appearing:
1. Make sure Web Render TOP is Active
2. Check URL is correct: http://localhost:3000/td-bidirectional.html
3. Enable mouse interaction on Web Render TOP
4. Click the START button in the rendered page

If no video appears:
1. Check browser permissions on remote device
2. Ensure both devices are on same network
3. Verify LiveKit credentials in .env file
4. Check OBS is receiving NDI stream

Your Railway deployment URL:
https://liquid-milk-balls-web-production-2e8c.up.railway.app/
    """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPress any key to exit...")
        input()
