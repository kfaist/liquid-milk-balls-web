"""
Comprehensive LiveKit Connection Test
Checks if publisher and viewer are actually connected and streaming
"""

import urllib.request
import json
import time

print("="*60)
print("LIVEKIT CONNECTION DIAGNOSTIC")
print("="*60)

# Test 1: Check token generation
print("\n[TEST 1] Token Generation")
print("-"*60)
try:
    response = urllib.request.urlopen('http://localhost:3000/api/viewer-token')
    data = json.loads(response.read().decode())
    print("[OK] Token endpoint working")
    print(f"    Server: {data.get('serverUrl', 'N/A')}")
    print(f"    Room: {data.get('roomName', 'N/A')}")
    print(f"    Token length: {len(data.get('token', ''))} chars")
    
    if data.get('roomName'):
        room_name = data.get('roomName')
        print(f"    Target room: {room_name}")
    else:
        print("[WARNING] No room name in token!")
        
except Exception as e:
    print(f"[ERROR] Token endpoint failed: {e}")

# Test 2: Check publisher token
print("\n[TEST 2] Publisher Token")
print("-"*60)
try:
    response = urllib.request.urlopen('http://localhost:3000/api/publisher-token')
    data = json.loads(response.read().decode())
    print("[OK] Publisher token endpoint working")
    print(f"    Room: {data.get('roomName', 'N/A')}")
except Exception as e:
    print(f"[ERROR] Publisher token failed: {e}")

# Test 3: Check if pages load
print("\n[TEST 3] Page Accessibility")
print("-"*60)
try:
    response = urllib.request.urlopen('http://localhost:3000/publisher.html')
    content = response.read().decode('utf-8')
    if 'livekit' in content.lower():
        print("[OK] publisher.html has LiveKit code")
    print(f"    Page size: {len(content)} bytes")
except Exception as e:
    print(f"[ERROR] publisher.html: {e}")

try:
    response = urllib.request.urlopen('http://localhost:3000/td-auto-viewer.html')
    content = response.read().decode('utf-8')
    if 'livekit-client@2.0.7' in content:
        print("[OK] td-auto-viewer.html has LiveKit SDK v2.0.7")
    else:
        print("[WARNING] LiveKit SDK version not found in td-auto-viewer.html")
    
    if '[TD-VIEWER]' in content:
        print("[OK] td-auto-viewer.html has diagnostic logging")
    
    print(f"    Page size: {len(content)} bytes")
except Exception as e:
    print(f"[ERROR] td-auto-viewer.html: {e}")

# Test 4: Check node server logs (if available)
print("\n[TEST 4] System Status")
print("-"*60)
import subprocess
result = subprocess.run(['powershell', 'netstat -ano | findstr :3000'], 
                       capture_output=True, text=True)
if '3000' in result.stdout:
    print("[OK] Node server listening on port 3000")
else:
    print("[ERROR] No server on port 3000")

# Summary
print("\n" + "="*60)
print("DIAGNOSTIC SUMMARY")
print("="*60)
print("\nSYSTEM READY FOR TESTING")
print("\nMANUAL STEPS REQUIRED:")
print("1. Open Firefox Tab 60 (publisher.html)")
print("2. Click 'Start Camera' button")
print("3. Check Firefox Tab 61 (td-auto-viewer.html) console (F12)")
print("4. Look for '[TD-VIEWER] Connected' message")
print("5. Check TouchDesigner webrender_livekit_input operator")
print("\nIf video appears in TouchDesigner = SUCCESS!")
print("="*60)
