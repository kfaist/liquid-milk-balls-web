"""
OBS Streaming Automation - Start WHIP Stream to LiveKit
"""

import subprocess
import time
import json

print("="*60)
print("OBS STREAMING SETUP - WHIP TO LIVEKIT")
print("="*60)

# Step 1: Check if OBS is running
print("\n[1/3] Checking OBS status...")
result = subprocess.run(['powershell', 'Get-Process | Where-Object {$_.ProcessName -like "*obs*"}'], 
                       capture_output=True, text=True)
if 'obs' in result.stdout.lower():
    print("[OK] OBS is running")
else:
    print("[ERROR] OBS not found. Please start OBS Studio first.")
    exit(1)

# Step 2: Check LiveKit WHIP endpoint
print("\n[2/3] Preparing WHIP stream configuration...")
print("WHIP Endpoint: https://claymation-transcription-l6e51sws.livekit.cloud")
print("Room: processed-output")
print("Bearer Token: Will use LiveKit API key")

# Step 3: Instructions for OBS setup
print("\n[3/3] OBS Streaming Instructions:")
print("="*60)
print("\nMANUAL STEPS (OBS doesn't have command-line streaming control):")
print("\n1. In OBS, go to: Settings → Stream")
print("2. Service: WHIP")
print("3. Server: https://claymation-transcription-l6e51sws.livekit.cloud")
print("4. Room: processed-output")
print("5. Bearer Token: Use your LiveKit API key")
print("\n6. Click 'Start Streaming' button in OBS")
print("\nOR - I can try to activate streaming programmatically...")

# Try to use OBS WebSocket (if enabled)
print("\n[ATTEMPTING] Programmatic stream start...")
print("Checking for OBS WebSocket...")

try:
    # Check if obs-websocket is available
    import obsws_python as obs_ws
    print("[INFO] OBS WebSocket library found, attempting connection...")
except ImportError:
    print("[INFO] OBS WebSocket not available via Python")
    print("[ACTION] Will use Windows automation to click 'Start Streaming' button")

print("\n" + "="*60)
print("NEXT: Activating OBS streaming via automation...")
print("="*60)
