"""
COMPLETE SYSTEM VERIFICATION AND CONFIGURATION
Run this to check everything and configure webrender1
"""
import subprocess
import time

print("=" * 80)
print("COMPLETE SYSTEM VERIFICATION")
print("=" * 80)

# Test 1: Check server is running
print("\n[TEST 1] Checking Node.js server...")
try:
    result = subprocess.run(['powershell', '-Command', 
                           'Get-Process node -ErrorAction SilentlyContinue | Select-Object -First 1'],
                          capture_output=True, text=True, timeout=5)
    if 'node' in result.stdout:
        print("PASS - Node.js server is running")
    else:
        print("FAIL - Node.js server not found")
except:
    print("ERROR - Could not check server")

# Test 2: Check pages are accessible
print("\n[TEST 2] Checking web pages...")
pages = [
    'http://localhost:3000/publisher.html',
    'http://localhost:3000/td-auto-viewer.html',
    'http://localhost:3000/return-viewer.html'
]

for page in pages:
    try:
        result = subprocess.run(['powershell', '-Command',
                               f'(Invoke-WebRequest -Uri "{page}" -UseBasicParsing).StatusCode'],
                              capture_output=True, text=True, timeout=5)
        if '200' in result.stdout:
            print(f"PASS - {page.split('/')[-1]}")
        else:
            print(f"FAIL - {page.split('/')[-1]}")
    except:
        print(f"ERROR - {page.split('/')[-1]}")

# Test 3: Check TouchDesigner is running
print("\n[TEST 3] Checking TouchDesigner...")
try:
    result = subprocess.run(['powershell', '-Command',
                           'Get-Process TouchDesigner -ErrorAction SilentlyContinue | Select-Object -First 1'],
                          capture_output=True, text=True, timeout=5)
    if 'TouchDesigner' in result.stdout:
        print("PASS - TouchDesigner is running")
    else:
        print("FAIL - TouchDesigner not running")
except:
    print("ERROR - Could not check TouchDesigner")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)

print("\n")
print("MANUAL CONFIGURATION NEEDED:")
print("=" * 80)
print("\nIn TouchDesigner, press Alt+T to open Textport, then paste this:")
print("")
print("wr=op('/webrender1');wr.par.active=0;import time;time.sleep(0.5);wr.par.active=1;wr.par.url='http://localhost:3000/td-auto-viewer.html';wr.par.reload.pulse();time.sleep(5);print('Result:',wr.width,'x',wr.height)")
print("")
print("Press Enter to execute")
print("")
print("=" * 80)
print("\nThen in browser (opening now):")
print("1. Go to: http://localhost:3000/publisher.html")
print("2. Click 'Start Publishing'")
print("3. Allow camera access")
print("")
print("=" * 80)

# Open publisher page
print("\nOpening publisher page in browser...")
subprocess.run(['powershell', '-Command', 'Start-Process "http://localhost:3000/publisher.html"'])
time.sleep(2)

print("\nDONE! Follow the manual steps above.")
