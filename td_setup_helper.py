"""
TouchDesigner WebRTC Setup Helper
Run this inside TouchDesigner's textport or as a Text DAT

This script helps set up the WebRTC/LiveKit integration in your TouchDesigner project.
"""

def setup_webrtc_input():
    """
    Sets up a Web Render TOP to receive remote video via LiveKit
    """
    print("Setting up WebRTC Input...")
    
    # Create Web Render TOP for input
    web_input = op('/').create(webRenderTOP, 'webrender_livekit_input')
    
    # Configure the Web Render TOP
    web_input.par.url = 'http://localhost:3000/td-auto-viewer.html'
    web_input.par.w = 1920
    web_input.par.h = 1080
    web_input.par.enableaudio = True
    web_input.par.active = True
    
    # Position it nicely
    web_input.nodeX = 0
    web_input.nodeY = 0
    
    print(f"✅ Created: {web_input.path}")
    print(f"   URL: {web_input.par.url}")
    print(f"   Resolution: {web_input.par.w} x {web_input.par.h}")
    print(f"   Audio: Enabled")
    
    return web_input


def setup_ndi_output(source_op=None):
    """
    Sets up NDI Out TOP to send processed video
    
    Args:
        source_op: The TOP operator to connect as input (optional)
    """
    print("\nSetting up NDI Output...")
    
    # Create NDI Out TOP
    ndi_out = op('/').create(ndioutTOP, 'ndiout_livekit_output')
    
    # Configure NDI Out
    ndi_out.par.active = True
    ndi_out.par.ndiname = 'TD-LiveKit-Output'
    ndi_out.par.w = 1920
    ndi_out.par.h = 1080
    ndi_out.par.fps = 30
    
    # Position it
    ndi_out.nodeX = 300
    ndi_out.nodeY = 0
    
    # Connect source if provided
    if source_op:
        ndi_out.inputConnectors[0].connect(source_op)
        print(f"   Connected input: {source_op.path}")
    
    print(f"✅ Created: {ndi_out.path}")
    print(f"   NDI Name: {ndi_out.par.ndiname}")
    print(f"   Resolution: {ndi_out.par.w} x {ndi_out.par.h}")
    print(f"   FPS: {ndi_out.par.fps}")
    
    return ndi_out


def create_complete_setup():
    """
    Creates the complete WebRTC bidirectional setup
    """
    print("=" * 60)
    print("TOUCHDESIGNER WEBRTC/LIVEKIT SETUP")
    print("=" * 60)
    
    # Create input
    web_input = setup_webrtc_input()
    
    # Create a simple processing example (Level TOP)
    print("\nSetting up simple processing example...")
    level = op('/').create(levelTOP, 'level_example')
    level.par.brightness = 1.2
    level.par.contrast = 1.1
    level.inputConnectors[0].connect(web_input)
    level.nodeX = 150
    level.nodeY = 0
    print(f"✅ Created: {level.path}")
    
    # Create output
    ndi_out = setup_ndi_output(level)
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Make sure your server is running at http://localhost:3000")
    print("2. Open publisher.html on a phone or another browser")
    print("3. Click 'Start Publishing' to send your camera to TouchDesigner")
    print("4. The webrender_livekit_input TOP will show the remote camera")
    print("5. Modify the processing network between input and output")
    print("6. NDI output will be available as 'TD-LiveKit-Output'")
    print("7. Capture this in OBS and publish via WHIP to LiveKit")
    print("\n" + "=" * 60)
    
    return {
        'input': web_input,
        'processing': level,
        'output': ndi_out
    }


def check_server():
    """
    Check if the local server is running
    """
    import urllib.request
    import urllib.error
    
    print("Checking if server is running...")
    
    try:
        response = urllib.request.urlopen('http://localhost:3000/healthz', timeout=2)
        if response.status == 200:
            print("✅ Server is running at http://localhost:3000")
            return True
    except urllib.error.URLError as e:
        print(f"❌ Server is not running!")
        print(f"   Error: {e}")
        print("\n   Start the server with:")
        print("   cd C:\\Users\\krista-showputer\\Desktop\\liquid-milk-balls-web")
        print("   npm start")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False


# Main execution
if __name__ == '__main__':
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  TouchDesigner WebRTC/LiveKit Setup Helper            ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Check server first
    if check_server():
        print("\n")
        response = input("Create complete WebRTC setup? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            ops = create_complete_setup()
            print("\n✅ All operators created successfully!")
            print(f"\nInput:  {ops['input'].path}")
            print(f"Process: {ops['processing'].path}")
            print(f"Output:  {ops['output'].path}")
        else:
            print("\nSetup cancelled. You can run individual functions:")
            print("  - setup_webrtc_input()")
            print("  - setup_ndi_output(source_op)")
            print("  - create_complete_setup()")
    else:
        print("\n❌ Please start the server first before setting up TouchDesigner")

