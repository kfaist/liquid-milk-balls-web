"""
Comprehensive System Test - WebRender TOP + LiveKit Integration
"""
import subprocess
import time
import requests

print("=" * 80)
print("SYSTEM TESTING - WebRender TOP + LiveKit")
print("=" * 80)
print()

# Test 1: Check if Node.js server is running
print("Test 1: Checking Node.js server on localhost:3000...")
try:
    response = requests.get('http://localhost:3000/publisher.html', timeout=5)
    if response.status_code == 200:
        print("[OK] Server is running and publisher.html is accessible")
        print(f"  Response code: {response.status_code}")
        print(f"  Content length: {len(response.content)} bytes")
    else:
        print(f"[FAIL] Server returned status code: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Server is not accessible: {e}")
print()

# Test 2: Check td-auto-viewer.html
print("Test 2: Checking td-auto-viewer.html...")
try:
    response = requests.get('http://localhost:3000/td-auto-viewer.html', timeout=5)
    if response.status_code == 200:
        print("[OK] td-auto-viewer.html is accessible")
        print(f"  Content length: {len(response.content)} bytes")
    else:
        print(f"[FAIL] td-auto-viewer.html returned status code: {response.status_code}")
except Exception as e:
    print(f"[FAIL] td-auto-viewer.html is not accessible: {e}")
print()

# Test 3: Check if TouchDesigner is running
print("Test 3: Checking TouchDesigner process...")
try:
    result = subprocess.run(
        ['powershell', '-Command', 
         'Get-Process | Where-Object {$_.ProcessName -eq "TouchDesigner"} | Select-Object Id, ProcessName'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if 'TouchDesigner' in result.stdout:
        print("[OK] TouchDesigner is running")
        print(result.stdout.strip())
    else:
        print("[FAIL] TouchDesigner is not running")
except Exception as e:
    print(f"[FAIL] Error checking TouchDesigner: {e}")
print()

# Test 4: Check if Firefox is running
print("Test 4: Checking Firefox process...")
try:
    result = subprocess.run(
        ['powershell', '-Command', 
         'Get-Process | Where-Object {$_.ProcessName -eq "firefox"} | Select-Object Id, ProcessName'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if 'firefox' in result.stdout:
        print("[OK] Firefox is running")
    else:
        print("[FAIL] Firefox is not running")
except Exception as e:
    print(f"[FAIL] Error checking Firefox: {e}")
print()

# Test 5: Open publisher page in default browser
print("Test 5: Opening publisher page...")
try:
    subprocess.run(
        ['powershell', '-Command', 'Start-Process "http://localhost:3000/publisher.html"'],
        timeout=5
    )
    print("[OK] Publisher page opened in browser")
    print("  URL: http://localhost:3000/publisher.html")
    print("  Please check browser to see if page loaded correctly")
    time.sleep(2)
except Exception as e:
    print(f"[FAIL] Error opening publisher page: {e}")
print()

# Test 6: Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print()
print("[OK] = Working")
print("[FAIL] = Needs attention")
print()
print("NEXT STEPS:")
print("1. Check Firefox to see if publisher.html loaded")
print("2. Click 'Start Publishing' button")
print("3. Allow camera access")
print("4. Check TouchDesigner WebRender TOP for video feed")
print("=" * 80)

# Save results to file
with open('test_results.txt', 'w') as f:
    f.write("System test completed\n")
    f.write("Check output above for details\n")

print("\nTest results saved to test_results.txt")
