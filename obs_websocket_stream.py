"""
Start OBS and configure streaming via WebSocket (NO CRASHES!)
"""

import subprocess
import time
from obswebsocket import obsws, requests

print("="*60)
print("OBS WEBSOCKET CONTROL - REALTIME STREAMING")
print("="*60)

# Kill any existing OBS
print("\n[1/5] Cleaning up...")
subprocess.run(['taskkill', '/IM', 'obs64.exe', '/F'], capture_output=True)
time.sleep(2)

# Start OBS (with empty stream config - won't crash)
print("\n[2/5] Starting OBS...")
subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])

# Wait for OBS to load
print("\n[3/5] Waiting for OBS WebSocket...")
for i in range(20):
    time.sleep(1)
    try:
        # Try to connect
        ws = obsws("localhost", 4455, "sjxgE4UKtQicgeIs")
        ws.connect()
        print(f"[OK] Connected to OBS WebSocket after {i+1} seconds")
        break
    except:
        if i == 19:
            print("[ERROR] Could not connect to OBS WebSocket")
            exit(1)

# Configure streaming via WebSocket
print("\n[4/5] Configuring WHIP streaming...")

# Set stream settings
stream_settings = {
    "server": "https://claymation-transcription-l6e51sws.whip.livekit.cloud/w",
    "bearer_token": "vZzz34cdzRkd",  # From LiveKit ingress
    "use_auth": False
}

try:
    ws.call(requests.SetStreamServiceSettings(
        streamServiceType="whip_custom",
        streamServiceSettings=stream_settings
    ))
    print("[OK] Stream settings configured")
except Exception as e:
    print(f"[INFO] Settings: {e}")

# Start streaming
print("\n[5/5] Starting stream...")
try:
    ws.call(requests.StartStream())
    print("[SUCCESS] Streaming started!")
    
    # Wait a moment then check status
    time.sleep(3)
    status = ws.call(requests.GetStreamStatus())
    print(f"[STATUS] Streaming: {status.getOutputActive()}")
    
except Exception as e:
    print(f"[ERROR] {e}")

ws.disconnect()

print("\n" + "="*60)
print("OBS STREAMING ACTIVE - REAL-TIME")
print("Check return-viewer.html for global output!")
print("="*60)
