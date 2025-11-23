"""
MASTER PIPELINE STARTUP SCRIPT
Automatically launches and configures the complete video processing pipeline
"""

import subprocess
import time
import sys
import os
import socket

# Paths
PROJECT_DIR = r"C:\Users\krista-showputer\Desktop\liquid-milk-balls-web"
OBS_PATH = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
TOUCHDESIGNER_CHECK = "TouchDesigner.exe"

# Server configuration
SERVER_PORT = 3000
WEBSOCKET_PORT = 4455

def print_header(text):
    """Print a section header"""
    print("\n" + "="*60)
    print(text)
    print("="*60)

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def is_process_running(process_name):
    """Check if a process is running"""
    result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'], 
                          capture_output=True, text=True)
    return process_name in result.stdout

def check_server():
    """Check if Node server is running"""
    print("\nChecking Node server...")
    if is_port_in_use(SERVER_PORT):
        print(f"  [OK] Server is running on port {SERVER_PORT}")
        return True
    else:
        print(f"  [WARN] Server is not running on port {SERVER_PORT}")
        print(f"  Starting server...")
        try:
            # Start server in background
            os.chdir(PROJECT_DIR)
            subprocess.Popen(['node', 'server.js'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE,
                           cwd=PROJECT_DIR)
            print("  Waiting for server to start...")
            time.sleep(5)
            
            if is_port_in_use(SERVER_PORT):
                print(f"  [OK] Server started successfully")
                return True
            else:
                print(f"  [FAIL] Server failed to start")
                return False
        except Exception as e:
            print(f"  [FAIL] Could not start server: {e}")
            return False

def check_touchdesigner():
    """Check if TouchDesigner is running"""
    print("\nChecking TouchDesigner...")
    if is_process_running(TOUCHDESIGNER_CHECK):
        print("  [OK] TouchDesigner is running")
        return True
    else:
        print("  [WARN] TouchDesigner is not running")
        print("  Please start TouchDesigner with your project file")
        return False

def check_obs():
    """Check if OBS is running, launch if needed"""
    print("\nChecking OBS Studio...")
    if is_process_running("obs64.exe"):
        print("  [OK] OBS is running")
        return True
    else:
        print("  [WARN] OBS is not running")
        print("  Launching OBS...")
        try:
            subprocess.Popen([OBS_PATH])
            print("  Waiting for OBS to start...")
            time.sleep(10)
            
            if is_process_running("obs64.exe"):
                print("  [OK] OBS started successfully")
                return True
            else:
                print("  [FAIL] OBS failed to start")
                return False
        except Exception as e:
            print(f"  [FAIL] Could not launch OBS: {e}")
            return False

def start_obs_stream():
    """Start OBS streaming via WebSocket"""
    print("\nStarting OBS stream...")
    
    try:
        from obsws_python import ReqClient
    except ImportError:
        print("  Installing obsws-python...")
        subprocess.run([sys.executable, "-m", "pip", "install", "obsws-python", "--break-system-packages"], 
                      check=True, capture_output=True)
        from obsws_python import ReqClient
    
    # Wait a bit for OBS WebSocket to be ready
    print("  Waiting for WebSocket server...")
    max_attempts = 10
    for attempt in range(max_attempts):
        if is_port_in_use(WEBSOCKET_PORT):
            break
        if attempt < max_attempts - 1:
            time.sleep(2)
    
    try:
        client = ReqClient(host="localhost", port=WEBSOCKET_PORT, password="", timeout=5)
        
        # Check if already streaming
        status = client.get_stream_status()
        if status.output_active:
            print("  [OK] Stream is already active")
            return True
        
        # Start streaming
        client.start_stream()
        time.sleep(2)
        
        # Verify
        status = client.get_stream_status()
        if status.output_active:
            print("  [OK] Stream started successfully")
            return True
        else:
            print("  [FAIL] Stream did not start")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Could not start stream: {e}")
        print("\n  MANUAL STEPS REQUIRED:")
        print("  1. In OBS, click 'Tools' > 'WebSocket Server Settings'")
        print("  2. Check: [X] Enable WebSocket server")
        print("  3. Port: 4455, Password: (leave empty)")
        print("  4. Click 'Start Streaming' in OBS")
        return False

def print_urls():
    """Print access URLs"""
    print_header("PIPELINE IS READY")
    print("\nAccess URLs:")
    print(f"  Camera Input:    http://localhost:{SERVER_PORT}/publisher.html")
    print(f"  Processed Video: http://localhost:{SERVER_PORT}/return-viewer.html")
    print("\nPipeline Flow:")
    print("  Browser Camera -> LiveKit (claymation-live)")
    print("  -> TouchDesigner (WebRender + Effects)")
    print("  -> NDI Output")
    print("  -> OBS Studio")
    print("  -> WHIP Stream")
    print("  -> LiveKit (processed-output)")
    print("  -> Browser Viewer")

def main():
    """Main pipeline startup sequence"""
    print_header("VIDEO PIPELINE STARTUP")
    print("This script will check and start all pipeline components\n")
    
    all_ok = True
    
    # Step 1: Check/start Node server
    if not check_server():
        all_ok = False
    
    # Step 2: Check TouchDesigner
    if not check_touchdesigner():
        print("\n  NOTE: TouchDesigner must be running with your project")
        print("  The pipeline will work once you start it")
    
    # Step 3: Check/start OBS
    if not check_obs():
        all_ok = False
    
    # Step 4: Start OBS stream
    if all_ok:
        if not start_obs_stream():
            all_ok = False
    
    # Print results
    if all_ok:
        print_urls()
        print("\n[SUCCESS] All systems ready!")
        return True
    else:
        print("\n" + "="*60)
        print("[INCOMPLETE] Some components need attention")
        print("="*60)
        print("\nPlease resolve the issues above and run this script again")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
