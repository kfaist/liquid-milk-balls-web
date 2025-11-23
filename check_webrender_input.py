"""
Check if webrender_livekit_input is showing video
"""

import sys

try:
    import td
except ImportError:
    print("Run from TouchDesigner Textport!")
    sys.exit(1)

print("=" * 60)
print("CHECKING CAMERA INPUT STATUS")
print("=" * 60)

# Get the webrender operator
webrender = op('/webrender_livekit_input')

if not webrender:
    print("ERROR: webrender_livekit_input not found!")
else:
    print("\n[STATUS] webrender_livekit_input")
    print("-" * 60)
    print(f"  Exists: YES")
    print(f"  Type: {webrender.type}")
    print(f"  Active: {webrender.par.active}")
    print(f"  URL: {webrender.par.url}")
    
    # Check if it has valid output
    if webrender.width > 0 and webrender.height > 0:
        print(f"  Resolution: {webrender.width}x{webrender.height}")
        print(f"  Has Video Output: YES")
    else:
        print(f"  Resolution: {webrender.width}x{webrender.height}")
        print(f"  Has Video Output: NO (black or not loaded)")
    
    # Open viewer to see it
    print("\n[ACTION] Opening viewer window...")
    webrender.openViewer()
    
    print("\n" + "=" * 60)
    print("WHAT TO CHECK:")
    print("=" * 60)
    print("""
Look at the viewer window that just opened:

IF YOU SEE BLACK:
  -> Open: http://localhost:3000/publisher.html
  -> Click 'Start Publishing'
  -> Allow camera access
  -> Wait 3-5 seconds
  -> You should see your camera in TouchDesigner!

IF YOU SEE YOUR CAMERA:
  -> SUCCESS! Input is working!
  -> Connect this to your effects
  -> Your effects output to NDI Out
  -> OBS receives NDI and streams to LiveKit
  -> Complete loop working!

The webrender_livekit_input is at: /webrender_livekit_input
Connect it to your processing network!
    """)
