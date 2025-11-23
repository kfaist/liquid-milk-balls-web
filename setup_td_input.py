"""
Add WebRender TOP to TouchDesigner for LiveKit camera input
This creates the INPUT path: Camera -> LiveKit -> WebRender TOP -> Effects
"""

import sys
import time

# TouchDesigner module
try:
    import td
except ImportError:
    print("This script must be run from TouchDesigner's textport")
    print("\nTo run:")
    print("1. Open TouchDesigner")
    print("2. Press Alt+T to open Textport")
    print("3. Type: exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/setup_td_input.py').read())")
    sys.exit(1)

print("=" * 60)
print("CREATING WEBRENDER TOP FOR CAMERA INPUT")
print("=" * 60)

# Create WebRender TOP for input
try:
    print("\n[1/5] Looking for existing webrender_livekit_input...")
    
    # Check if it already exists
    existing = op('/webrender_livekit_input')
    if existing:
        print("Found existing webrender_livekit_input operator")
        webrender = existing
    else:
        print("Creating new webrender_livekit_input operator...")
        webrender = root.create(webRenderTOP, 'webrender_livekit_input')
        print("Created webrender_livekit_input!")
    
    # Configure the WebRender TOP
    print("\n[2/5] Configuring WebRender TOP...")
    webrender.par.url = 'http://localhost:3000/td-auto-viewer.html'
    webrender.par.active = True
    webrender.par.w = 1920
    webrender.par.h = 1080
    webrender.par.reload.pulse()
    print("Configuration applied:")
    print("  URL: http://localhost:3000/td-auto-viewer.html")
    print("  Active: ON")
    print("  Resolution: 1920x1080")
    
    # Position it nicely in the network
    print("\n[3/5] Positioning operator...")
    webrender.nodeX = -200
    webrender.nodeY = 200
    print("Positioned at (-200, 200)")
    
    # Add note
    print("\n[4/5] Adding documentation...")
    webrender.comment = """
CAMERA INPUT FROM LIVEKIT
This WebRender TOP loads td-auto-viewer.html
which receives the LiveKit camera stream.

Connect this to your effects processing!
    """
    print("Added operator comment")
    
    # Show the result
    print("\n[5/5] Opening viewer...")
    webrender.openViewer()
    print("Viewer window opened!")
    
    print("\n" + "=" * 60)
    print("SUCCESS! WEBRENDER TOP CREATED")
    print("=" * 60)
    print("""
Next Steps:
1. Wait for LiveKit upgrade to complete
2. Open publisher.html in browser
3. Click 'Start Publishing'
4. This WebRender TOP will show the camera!
5. Connect it to your effects processing
6. Your NDI Out will send processed video to OBS

The complete loop will be:
Camera -> WebRender TOP -> Effects -> NDI Out -> OBS -> Viewer
    """)
    
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nTroubleshooting:")
    print("- Make sure you're running this in TouchDesigner's Textport")
    print("- Press Alt+T to open Textport")
    print("- Then run: exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/setup_td_input.py').read())")
