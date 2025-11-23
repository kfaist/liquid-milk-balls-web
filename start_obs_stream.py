"""
OBS Stream Starter - Simple WebSocket Control
"""

import sys
import time

try:
    from obsws_python import ReqClient
except ImportError:
    print("Installing obsws-python...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "obsws-python", "--break-system-packages"], check=True)
    from obsws_python import ReqClient

WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 4455

def test_connection():
    """Test WebSocket connection"""
    print("Testing OBS WebSocket connection...")
    try:
        client = ReqClient(host=WEBSOCKET_HOST, port=WEBSOCKET_PORT, password="", timeout=5)
        print("[OK] WebSocket connected successfully!")
        return client
    except Exception as e:
        print(f"[FAIL] WebSocket connection failed: {e}")
        return None

def start_streaming(client):
    """Start OBS streaming"""
    try:
        # Check if already streaming
        status = client.get_stream_status()
        if status.output_active:
            print("[OK] Stream is already active!")
            return True
        
        # Start streaming
        print("Starting stream...")
        client.start_stream()
        time.sleep(2)
        
        # Verify it started
        status = client.get_stream_status()
        if status.output_active:
            print("[OK] Stream started successfully!")
            print(f"   Duration: {status.output_duration / 1000:.1f}s")
            print(f"   Bytes sent: {status.output_bytes}")
            return True
        else:
            print("[FAIL] Stream did not start")
            return False
            
    except Exception as e:
        print(f"[FAIL] Failed to start stream: {e}")
        return False

def main():
    print("="*60)
    print("OBS STREAM STARTER")
    print("="*60)
    
    # Test connection
    client = test_connection()
    
    if client is None:
        print("\n" + "="*60)
        print("MANUAL SETUP REQUIRED")
        print("="*60)
        print("\nWebSocket is not enabled in OBS. Follow these steps:")
        print("\n1. In OBS, click 'Tools' in the top menu")
        print("2. Click 'WebSocket Server Settings'")
        print("3. Check the box: [X] Enable WebSocket server")
        print("4. Leave the password field EMPTY")
        print("5. Make sure Port is: 4455")
        print("6. Click 'OK'")
        print("\nThen run this script again!")
        return False
    
    # Start streaming
    success = start_streaming(client)
    
    if success:
        print("\n" + "="*60)
        print("[SUCCESS] OBS IS NOW STREAMING!")
        print("="*60)
        print("\nYour video pipeline is active:")
        print("  Camera -> LiveKit -> TouchDesigner -> OBS -> LiveKit")
        print("\nNext steps:")
        print("  1. Open: http://localhost:3000/publisher.html (camera input)")
        print("  2. Open: http://localhost:3000/return-viewer.html (view output)")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
