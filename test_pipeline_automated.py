"""
Automated Pipeline Test Script
Tests publisher -> viewer -> TouchDesigner pipeline
"""

import subprocess
import time
import json
import urllib.request
import urllib.error

print("="*60)
print("AUTOMATED PIPELINE TEST")
print("="*60)

# Test 1: Verify Node Server
print("\n[1/5] Checking Node server...")
try:
    response = urllib.request.urlopen('http://localhost:3000/api/viewer-token')
    data = json.loads(response.read().decode())
    print("[OK] Node server running")
    print(f"   Room: {data.get('roomName')}")
    print(f"   Server: {data.get('serverUrl')}")
    token_works = True
except Exception as e:
    print(f"[ERROR] Node server error: {e}")
    token_works = False

# Test 2: Check LiveKit SDK version in td-auto-viewer.html
print("\n[2/5] Checking td-auto-viewer.html fix...")
try:
    with open(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td-auto-viewer.html', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'livekit-client@2.0.7' in content:
            print("[OK] LiveKit SDK v2.0.7 confirmed in file")
            sdk_fixed = True
        else:
            print("[ERROR] LiveKit SDK version not found")
            sdk_fixed = False
except Exception as e:
    print(f"[ERROR] Cannot read file: {e}")
    sdk_fixed = False

# Test 3: Verify pages are accessible
print("\n[3/5] Testing page accessibility...")
try:
    urllib.request.urlopen('http://localhost:3000/publisher.html')
    print("[OK] publisher.html accessible")
    publisher_ok = True
except:
    print("[ERROR] publisher.html not accessible")
    publisher_ok = False

try:
    urllib.request.urlopen('http://localhost:3000/td-auto-viewer.html')
    print("[OK] td-auto-viewer.html accessible")
    viewer_ok = True
except:
    print("[ERROR] td-auto-viewer.html not accessible")
    viewer_ok = False

# Test 4: Check if TouchDesigner is running
print("\n[4/5] Checking TouchDesigner...")
result = subprocess.run(['powershell', 'Get-Process | Where-Object {$_.ProcessName -like "*TouchDesigner*"} | Select-Object ProcessName'], 
                       capture_output=True, text=True)
if 'TouchDesigner' in result.stdout:
    print("[OK] TouchDesigner is running")
    td_running = True
else:
    print("[WARNING] TouchDesigner not detected (may be named differently)")
    td_running = False

# Test 5: Summary
print("\n[5/5] Test Summary")
print("="*60)
if token_works and sdk_fixed and publisher_ok and viewer_ok:
    print("[SUCCESS] All critical systems ready!")
else:
    print("[WARNING] Some issues detected, check above")

print("\nNEXT STEPS FOR MANUAL TESTING:")
print("1. Go to Firefox Tab with publisher.html")
print("2. Click 'Start Camera' button")
print("3. Go to Tab with td-auto-viewer.html") 
print("4. Press F12 and check console for '[TD-VIEWER] Connected'")
print("5. In TouchDesigner, reload webrender with Textport command:")
print("   op('/webrender_livekit_input').par.reload.pulse()")
print("="*60)
