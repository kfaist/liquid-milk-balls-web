# Create a minimal TouchDesigner Python setup that saves to a new .toe file
# This script creates the operators and then saves the file

import os
import sys

# Add TouchDesigner Python path if running inside TD
# If running outside, this will fail gracefully

try:
    # This will only work if running inside TouchDesigner
    root = op('/')
    
    print("="*60)
    print("CREATING WEBRTC OPERATORS IN TOUCHDESIGNER")
    print("="*60)
    
    # Clean up any existing
    for name in ['webrender_livekit_input', 'ndiout_livekit']:
        if op('/' + name):
            op('/' + name).destroy()
            print(f"Removed existing: {name}")
    
    # Create Web Render TOP
    print("\nCreating Web Render TOP...")
    web = root.create(webrenderTOP, 'webrender_livekit_input')
    web.par.url = 'http://localhost:3000/td-auto-viewer.html'
    web.par.resolution = [1920, 1080]
    web.par.enableaudio = True
    web.par.active = True
    web.nodeX = -200
    web.nodeY = 200
    print(f"✅ Created: {web.path}")
    
    # Create NDI Out TOP
    print("\nCreating NDI Out TOP...")
    ndi = root.create(ndioutTOP, 'ndiout_livekit')
    ndi.par.active = True
    ndi.par.ndiname = 'TD-LiveKit-Output'
    ndi.nodeX = 200
    ndi.nodeY = 200
    print(f"✅ Created: {ndi.path}")
    
    # Connect them
    print("\nConnecting operators...")
    ndi.inputConnectors[0].connect(web)
    print(f"✅ Connected: {web.path} → {ndi.path}")
    
    # Save the file
    print("\nSaving file...")
    project.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrtc-ready.toe')
    print("✅ Saved to: webrtc-ready.toe")
    
    print("\n" + "="*60)
    print("SUCCESS! File saved with WebRTC operators")
    print("="*60)
    print("\nTo use:")
    print("1. Open webrtc-ready.toe in TouchDesigner")
    print("2. Start publisher: http://192.168.24.70:3000/publisher.html")
    print("3. Add NDI source 'TD-LiveKit-Output' in OBS")
    
except NameError:
    print("ERROR: This script must be run inside TouchDesigner!")
    print("Copy this file content and paste into a Text DAT in TouchDesigner")
    print("Then in another Text DAT, put: exec(op('text1').text)")
