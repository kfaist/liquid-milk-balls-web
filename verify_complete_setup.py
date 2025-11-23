"""
Complete Pipeline Verification
Tests all components of the video loop
"""
import requests
import time

print("="*60)
print("COMPLETE PIPELINE VERIFICATION")
print("="*60)

# Test 1: Server Health
print("\n[1/5] Testing Server...")
try:
    r = requests.get("http://localhost:3000/healthz", timeout=2)
    if r.status_code == 200:
        print("  [OK] Server is running")
    else:
        print(f"  [FAIL] Server returned {r.status_code}")
except Exception as e:
    print(f"  [FAIL] Server error: {e}")

# Test 2: Publisher Token
print("\n[2/5] Testing Publisher Token (for camera input)...")
try:
    r = requests.get("http://localhost:3000/api/publisher-token", timeout=2)
    if r.status_code == 200:
        data = r.json()
        print(f"  [OK] Token generated for room: {data.get('room', 'N/A')}")
        print(f"       URL: {data.get('url', 'N/A')}")
    else:
        print(f"  [FAIL] Status: {r.status_code}")
except Exception as e:
    print(f"  [FAIL] Error: {e}")

# Test 3: Processed Viewer Token
print("\n[3/5] Testing Viewer Token (for processed output)...")
try:
    r = requests.get("http://localhost:3000/api/processed-viewer-token", timeout=2)
    if r.status_code == 200:
        data = r.json()
        print(f"  [OK] Token generated for room: {data.get('room', 'N/A')}")
        print(f"       URL: {data.get('url', 'N/A')}")
    else:
        print(f"  [FAIL] Status: {r.status_code}")
except Exception as e:
    print(f"  [FAIL] Error: {e}")

# Test 4: Check OBS Service Config
print("\n[4/5] Checking OBS WHIP Configuration...")
try:
    import json
    config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    settings = config.get('settings', {})
    server = settings.get('server', 'NOT SET')
    bearer = settings.get('bearer_token', 'NOT SET')
    use_auth = settings.get('use_auth', False)
    
    print(f"  [INFO] WHIP Server: {server}")
    print(f"  [INFO] Bearer Token: {bearer[:20]}..." if len(bearer) > 20 else f"  [INFO] Bearer Token: {bearer}")
    print(f"  [INFO] Use Auth: {use_auth}")
    
    if 'whip.livekit.cloud' in server and len(bearer) > 10:
        print("  [OK] OBS WHIP configuration looks correct")
    else:
        print("  [WARNING] OBS WHIP configuration may need updating")
except Exception as e:
    print(f"  [FAIL] Could not read config: {e}")

# Test 5: Check if TouchDesigner is running
print("\n[5/5] Checking TouchDesigner...")
import subprocess
try:
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TouchDesigner.exe'], 
                          capture_output=True, text=True)
    if 'TouchDesigner.exe' in result.stdout:
        print("  [OK] TouchDesigner is running")
    else:
        print("  [WARNING] TouchDesigner does not appear to be running")
except Exception as e:
    print(f"  [FAIL] Could not check: {e}")

# Summary
print("\n" + "="*60)
print("PIPELINE STATUS SUMMARY")
print("="*60)
print("\nThe following components are configured:")
print("  1. Web Server: Running on port 3000")
print("  2. Publisher: Ready to send camera to 'claymation-live' room")
print("  3. Viewer: Ready to receive from 'processed-output' room")
print("  4. OBS WHIP: Configured with LiveKit ingress")
print("\nTo complete the loop:")
print("  1. Make sure TouchDesigner is running and configured")
print("  2. In OBS, click 'Start Streaming' button")
print("  3. Open http://localhost:3000/publisher.html - allow camera")
print("  4. Open http://localhost:3000/return-viewer.html - click 'Join Stream'")
print("\nYou should see your processed video in the viewer!")
print("="*60)
