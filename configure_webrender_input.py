"""
Configure the existing webrender_livekit_input for camera input
"""

import sys

try:
    import td
except ImportError:
    print("Run this from TouchDesigner Textport!")
    sys.exit(1)

print("=" * 60)
print("CONFIGURING WEBRENDER_LIVEKIT_INPUT")
print("=" * 60)

# Get the existing operator
webrender = op('/webrender_livekit_input')

if not webrender:
    print("ERROR: webrender_livekit_input not found!")
else:
    print("\n[1/4] Found webrender_livekit_input!")
    
    print("\n[2/4] Setting URL to td-auto-viewer.html...")
    webrender.par.url = 'http://localhost:3000/td-auto-viewer.html'
    print("  URL: http://localhost:3000/td-auto-viewer.html")
    
    print("\n[3/4] Activating...")
    webrender.par.active = True
    print("  Active: ON")
    
    print("\n[4/4] Reloading page...")
    webrender.par.reload.pulse()
    print("  Page reloaded!")
    
    print("\n" + "=" * 60)
    print("SUCCESS! CAMERA INPUT CONFIGURED")
    print("=" * 60)
    print("""
NEXT STEPS:

1. Open in browser: http://localhost:3000/publisher.html
2. Click 'Start Publishing'
3. Allow camera access
4. Look at webrender_livekit_input in TouchDesigner
5. You should see your camera!

Then the complete loop:
Camera -> webrender_livekit_input -> Your Effects -> NDI Out -> OBS -> Viewer

Let's test it!
    """)
