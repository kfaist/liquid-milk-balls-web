"""
Quick OBS WebSocket - Just Start Streaming
"""

from obswebsocket import obsws, requests
import time

try:
    print("Connecting to OBS...")
    ws = obsws("localhost", 4455, "sjxgE4UKtQicgeIs")
    ws.connect()
    print("[OK] Connected!")
    
    print("Starting stream...")
    ws.call(requests.StartStream())
    print("[SUCCESS] Stream started!")
    
    time.sleep(2)
    status = ws.call(requests.GetStreamStatus())
    print(f"Streaming: {status.getOutputActive()}")
    
    ws.disconnect()
except Exception as e:
    print(f"Error: {e}")
