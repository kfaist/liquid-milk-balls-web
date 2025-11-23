"""
Systematic WebRender Testing - Run from TouchDesigner Textport
Tests multiple pages to identify the issue
"""

import sys
import time

try:
    import td
except ImportError:
    print("ERROR: Must run from TouchDesigner Textport")
    sys.exit(1)

print("=" * 70)
print("SYSTEMATIC WEBRENDER TESTING")
print("=" * 70)

webrender = op('/webrender_livekit_input')

if not webrender:
    print("ERROR: webrender_livekit_input not found!")
    sys.exit(1)

# Test sequence
tests = [
    ("Simple gradient test", "http://localhost:3000/simple-test.html"),
    ("WebRender test (green)", "http://localhost:3000/webrender-test.html"),
    ("LiveKit viewer page", "http://localhost:3000/td-auto-viewer.html"),
]

results = []

for test_name, url in tests:
    print(f"\n[TEST] {test_name}")
    print(f"URL: {url}")
    print("-" * 70)
    
    # Configure WebRender
    webrender.par.active = False
    time.sleep(0.5)
    webrender.par.active = True
    webrender.par.url = url
    time.sleep(1)
    webrender.par.reload.pulse()
    
    # Wait for page to load
    print("Waiting 4 seconds for page load...")
    time.sleep(4)
    
    # Check result
    width = webrender.width
    height = webrender.height
    
    if width > 0 and height > 0:
        print(f"PASS - Resolution: {width}x{height}")
        results.append((test_name, "PASS", f"{width}x{height}"))
    else:
        print(f"FAIL - No output (width={width}, height={height})")
        results.append((test_name, "FAIL", "No output"))
    
    time.sleep(2)

# Summary
print("\n" + "=" * 70)
print("TEST RESULTS SUMMARY")
print("=" * 70)

for test_name, status, detail in results:
    status_symbol = "✓" if status == "PASS" else "✗"
    print(f"{status_symbol} {test_name:30} | {status:4} | {detail}")

# Diagnosis
print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70)

all_pass = all(status == "PASS" for _, status, _ in results)
all_fail = all(status == "FAIL" for _, status, _ in results)

if all_fail:
    print("""
ALL TESTS FAILED!

This means TouchDesigner WebRender is not working at all.

Possible causes:
1. WebRender component needs initialization
2. Security/permission issue with localhost
3. TouchDesigner WebRender not properly installed

Solution:
Try creating a NEW Web Render TOP:
- Press Tab in network editor
- Type 'webrender' 
- Create fresh Web Render TOP
- Set URL to: http://localhost:3000/simple-test.html
- Enable Active
    """)
elif all_pass:
    print("""
ALL TESTS PASSED!

WebRender is working perfectly!

Your webrender_livekit_input is now configured with:
URL: http://localhost:3000/td-auto-viewer.html

Next steps:
1. Open browser: http://localhost:3000/publisher.html
2. Click 'Start Publishing'
3. Allow camera
4. Watch webrender_livekit_input - camera should appear!
    """)
else:
    print("""
MIXED RESULTS!

Some pages work, some don't.

This means WebRender works, but td-auto-viewer.html has an issue.

Possible causes:
1. LiveKit JavaScript error
2. Page needs more time to load
3. LiveKit connection issue

Check browser console on td-auto-viewer.html for errors.
    """)

# Keep it on the working page if available
if results[-1][1] == "PASS":
    print(f"\nWebRender left on: {tests[-1][0]}")
else:
    # Try to leave it on a working page
    for i, (test_name, status, _) in enumerate(results):
        if status == "PASS":
            webrender.par.url = tests[i][1]
            webrender.par.reload.pulse()
            print(f"\nWebRender set to working page: {test_name}")
            break
