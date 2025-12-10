"""
Slider Bridge - Polls Railway server and sends to TouchDesigner via UDP
"""
import json
import socket
import time
import urllib.request
import sys

SLIDER_URL = "https://adequate-balance-production.up.railway.app/api/sliders"
TD_HOST = "127.0.0.1"
TD_PORT = 8021

print("=" * 50, flush=True)
print("SLIDER BRIDGE STARTING", flush=True)
print("=" * 50, flush=True)
print(f"Polling: {SLIDER_URL}", flush=True)
print(f"Sending UDP to: {TD_HOST}:{TD_PORT}", flush=True)
print("Press Ctrl+C to stop", flush=True)
print("=" * 50, flush=True)
sys.stdout.flush()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_sliders = None
count = 0

while True:
    try:
        with urllib.request.urlopen(SLIDER_URL, timeout=3) as response:
            data = response.read().decode()
            sliders = json.loads(data)
            count += 1
            
            # Send every time (TD will ignore duplicates if needed)
            sock.sendto(data.encode(), (TD_HOST, TD_PORT))
            
            if count % 10 == 1:  # Print every ~1 second
                print(f"[{count}] hue={sliders.get('hue')} sat={sliders.get('sat')} depth={sliders.get('depth')} photo={sliders.get('photorealism')} -> UDP:{TD_PORT}", flush=True)
                
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
    
    time.sleep(0.1)
