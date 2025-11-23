"""
Complete WebRender diagnostic and fix
"""

import sys
import time

try:
    import td
except ImportError:
    print("Run from TouchDesigner Textport!")
    sys.exit(1)

print("=" * 60)
print("WEBRENDER DIAGNOSTIC & FIX")
print("=" * 60)

webrender = op('/webrender_livekit_input')

# Step 1: Test with simple page
print("\n[STEP 1] Testing WebRender with simple green page...")
webrender.par.active = True
webrender.par.url = 'http://localhost:3000/webrender-test.html'
webrender.par.reload.pulse()
time.sleep(3)

if webrender.width > 0 and webrender.height > 0:
    print("  SUCCESS! WebRender CAN load pages")
    print(f"  Resolution: {webrender.width}x{webrender.height}")
    webrender.openViewer()
    print("  You should see GREEN screen")
else:
    print("  FAIL! WebRender can't load any pages")
    print("  This is a TouchDesigner WebRender issue, not our page")

# Step 2: Try the actual LiveKit viewer
print("\n[STEP 2] Loading td-auto-viewer.html...")
time.sleep(2)
webrender.par.url = 'http://localhost:3000/td-auto-viewer.html'
webrender.par.reload.pulse()
time.sleep(3)

if webrender.width > 0 and webrender.height > 0:
    print("  SUCCESS! td-auto-viewer.html loaded")
    print(f"  Resolution: {webrender.width}x{webrender.height}")
else:
    print("  td-auto-viewer.html not rendering")
    print("  Trying toggle fix...")
    webrender.par.active = False
    time.sleep(1)
    webrender.par.active = True
    time.sleep(2)
    webrender.par.reload.pulse()
    time.sleep(3)
    
    if webrender.width > 0:
        print("  Fixed with toggle!")
    else:
        print("  Still not working - may need browser console check")

# Step 3: Final status
print("\n" + "=" * 60)
print("FINAL STATUS")
print("=" * 60)
print(f"Active: {webrender.par.active}")
print(f"URL: {webrender.par.url}")
print(f"Resolution: {webrender.width}x{webrender.height}")

if webrender.width > 0:
    print("\nSTATUS: WORKING!")
    print("""
Next steps:
1. Open http://localhost:3000/publisher.html in BROWSER
2. Click 'Start Publishing'
3. Allow camera
4. Wait 5 seconds
5. Look at webrender_livekit_input in TouchDesigner
6. You should see your camera!
    """)
else:
    print("\nSTATUS: NOT WORKING")
    print("""
WebRender is not rendering the page.
This could be:
- JavaScript error on page
- LiveKit connection issue
- TouchDesigner WebRender security restriction

Check browser console on td-auto-viewer.html for errors.
    """)
