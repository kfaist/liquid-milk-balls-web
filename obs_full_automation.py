"""
OBS Full Automation Script
Handles launching OBS, enabling WebSocket if needed, and starting stream
"""

import subprocess
import time
import sys
import os

try:
    import pyautogui
    import obsws_python as obs
    from obsws_python import ReqClient
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui", "obsws-python", "--break-system-packages"], check=True)
    import pyautogui
    import obsws_python as obs
    from obsws_python import ReqClient

# Configuration
OBS_PATH = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 4455
MAX_RETRIES = 30
RETRY_DELAY = 2

def is_obs_running():
    """Check if OBS is already running"""
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'], 
                          capture_output=True, text=True)
    return 'obs64.exe' in result.stdout

def launch_obs():
    """Launch OBS if not already running"""
    if is_obs_running():
        print("OBS is already running")
        return True
    
    print("Launching OBS...")
    try:
        subprocess.Popen([OBS_PATH], shell=False)
        print("OBS launch command sent. Waiting for application to start...")
        time.sleep(10)  # Give OBS time to fully launch
        return True
    except Exception as e:
        print(f"Failed to launch OBS: {e}")
        return False

def try_websocket_connection(retries=MAX_RETRIES):
    """Try to connect to OBS WebSocket"""
    print(f"Attempting to connect to OBS WebSocket on {WEBSOCKET_HOST}:{WEBSOCKET_PORT}...")
    
    for attempt in range(retries):
        try:
            client = ReqClient(host=WEBSOCKET_HOST, port=WEBSOCKET_PORT, password="")
            print("✓ WebSocket connection successful!")
            return client
        except Exception as e:
            if attempt < retries - 1:
                print(f"Connection attempt {attempt + 1}/{retries} failed. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"✗ WebSocket connection failed after {retries} attempts")
                return None

def enable_websocket_via_gui():
    """Use GUI automation to enable WebSocket in OBS"""
    print("\n=== ENABLING WEBSOCKET VIA GUI AUTOMATION ===")
    print("This will click through the OBS menus to enable WebSocket...")
    time.sleep(2)
    
    try:
        # Click on Tools menu
        print("Step 1: Clicking 'Tools' menu...")
        pyautogui.click(x=100, y=50)  # Approximate location, may need adjustment
        time.sleep(1)
        
        # Type to search for WebSocket option
        print("Step 2: Looking for WebSocket Server Settings...")
        pyautogui.typewrite('websocket', interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        
        # Enable WebSocket checkbox
        print("Step 3: Enabling WebSocket server...")
        pyautogui.press('space')  # Toggle checkbox
        time.sleep(1)
        
        # Click OK
        print("Step 4: Saving settings...")
        pyautogui.press('enter')
        time.sleep(2)
        
        print("✓ GUI automation completed")
        return True
        
    except Exception as e:
        print(f"✗ GUI automation failed: {e}")
        return False

def start_streaming(client):
    """Start OBS streaming"""
    try:
        print("\n=== STARTING STREAM ===")
        client.start_stream()
        print("✓ Stream started successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to start stream: {e}")
        return False

def main():
    """Main automation workflow"""
    print("="*60)
    print("OBS FULL AUTOMATION SCRIPT")
    print("="*60)
    
    # Step 1: Launch OBS
    if not launch_obs():
        print("\n✗ FAILED: Could not launch OBS")
        return False
    
    # Step 2: Try WebSocket connection
    client = try_websocket_connection()
    
    # Step 3: If WebSocket failed, enable it via GUI
    if client is None:
        print("\nWebSocket not available. Attempting to enable it via GUI...")
        if enable_websocket_via_gui():
            print("\nRetrying WebSocket connection after GUI enable...")
            time.sleep(5)
            client = try_websocket_connection(retries=10)
        
        if client is None:
            print("\n✗ FAILED: Could not establish WebSocket connection")
            print("\nMANUAL INTERVENTION REQUIRED:")
            print("1. In OBS, go to: Tools → WebSocket Server Settings")
            print("2. Check: ☑ Enable WebSocket server")
            print("3. Leave password field EMPTY")
            print("4. Port: 4455")
            print("5. Click OK")
            print("6. Run this script again")
            return False
    
    # Step 4: Start streaming
    if start_streaming(client):
        print("\n" + "="*60)
        print("✓ SUCCESS: OBS is now streaming to LiveKit!")
        print("="*60)
        print("\nNext steps:")
        print("1. Open publisher.html to start camera input")
        print("2. Open return-viewer.html to view processed output")
        return True
    else:
        print("\n✗ FAILED: Could not start stream")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
