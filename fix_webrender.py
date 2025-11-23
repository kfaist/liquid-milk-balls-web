"""
Fix webrender_livekit_input loading issue
"""

import sys
import time

try:
    import td
except ImportError:
    print("Run from TouchDesigner Textport!")
    sys.exit(1)

print("=" * 60)
print("TROUBLESHOOTING WEBRENDER INPUT")
print("=" * 60)

webrender = op('/webrender_livekit_input')

if not webrender:
    print("ERROR: webrender_livekit_input not found!")
else:
    print("\n[1/6] Current settings:")
    print(f"  Active: {webrender.par.active}")
    print(f"  URL: {webrender.par.url}")
    
    print("\n[2/6] Checking resolution...")
    print(f"  Width: {webrender.width}")
    print(f"  Height: {webrender.height}")
    
    print("\n[3/6] Forcing reload...")
    webrender.par.reload.pulse()
    print("  Reload triggered!")
    
    print("\n[4/6] Waiting 3 seconds...")
    import time
    time.sleep(3)
    
    print("\n[5/6] Checking again...")
    print(f"  Width: {webrender.width}")
    print(f"  Height: {webrender.height}")
    
    if webrender.width > 0 and webrender.height > 0:
        print("  SUCCESS! WebRender has valid output")
    else:
        print("  STILL BLACK - trying alternative fix...")
        
        # Try toggling active off/on
        print("\n[6/6] Toggling active state...")
        webrender.par.active = False
        time.sleep(1)
        webrender.par.active = True
        time.sleep(2)
        webrender.par.reload.pulse()
        time.sleep(2)
        
        print(f"  Final width: {webrender.width}")
        print(f"  Final height: {webrender.height}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    
    if webrender.width > 0:
        print("""
SUCCESS! WebRender is working!

Now:
1. Open: http://localhost:3000/publisher.html
2. Click 'Start Publishing'
3. Allow camera
4. Watch webrender_livekit_input in TouchDesigner
5. You should see your camera appear!
        """)
    else:
        print("""
WebRender still showing error. Possible issues:

1. Server page has JavaScript errors
   -> Check browser console on td-auto-viewer.html
   
2. TouchDesigner WebRender security restrictions
   -> Try setting URL to a simple test page first
   
3. LiveKit connection issue
   -> Check if publisher.html works in regular browser

Let me check the server page for errors...
        """)
