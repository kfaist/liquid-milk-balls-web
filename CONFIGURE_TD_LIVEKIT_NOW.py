"""
TOUCHDESIGNER LIVEKIT CONFIGURATION SCRIPT
Run this INSIDE TouchDesigner's textport to configure WebRTC/LiveKit
"""

# Step 1: Create Web Render TOP for receiving video
webrender_input = op('/').create(webRenderTOP, 'webrender_livekit_input')

# Step 2: Configure it to use the viewer page which connects to LiveKit
webrender_input.par.url = 'https://liquid-milk-balls-web-production-2e8c.up.railway.app/td-auto-viewer.html'
webrender_input.par.w = 1920
webrender_input.par.h = 1080
webrender_input.par.fps = 30

# Enable it
webrender_input.par.active = True

print("=" * 60)
print("TOUCHDESIGNER LIVEKIT SETUP COMPLETE!")
print("=" * 60)
print("")
print("✓ Created webrender_livekit_input TOP")
print("✓ Configured to receive from LiveKit")
print("")
print("NEXT STEPS:")
print("1. The Web Render TOP should auto-connect to LiveKit")
print("2. When someone publishes at:")
print("   https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html")
print("3. Video will appear in the webrender_livekit_input TOP")
print("")
print("CONNECT IT:")
print("webrender_livekit_input → Your Effects → NDI Out")
print("=" * 60)
