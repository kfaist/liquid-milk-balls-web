"""
TouchDesigner WebRTC Setup - Execution Script (FIXED)
This script will be executed directly in TouchDesigner
"""

import json

def get_current_operators():
    """Get list of all current operators in the root"""
    ops_list = []
    for child in op('/').children:
        ops_list.append({
            'name': child.name,
            'type': child.type,
            'path': child.path
        })
    return ops_list

def setup_webrtc_receiver():
    """Create and configure Web Render TOP for receiving WebRTC stream"""
    
    print("\n" + "="*60)
    print("SETTING UP WEBRTC RECEIVER")
    print("="*60)
    
    # Check if it already exists
    if op('/webrender_livekit_input'):
        print("⚠️  webrender_livekit_input already exists, using existing operator")
        web_input = op('/webrender_livekit_input')
    else:
        # Create Web Render TOP (lowercase: webrendertop)
        print("\n1. Creating Web Render TOP...")
        web_input = op('/').create(webrendertop, 'webrender_livekit_input')
        print(f"   ✅ Created: {web_input.path}")
    
    # Configure it
    print("\n2. Configuring Web Render TOP...")
    web_input.par.url = 'http://localhost:3000/td-auto-viewer.html'
    web_input.par.w = 1920
    web_input.par.h = 1080
    web_input.par.enableaudio = True
    web_input.par.active = True
    
    # Position it
    web_input.nodeX = -200
    web_input.nodeY = 200
    
    print(f"   URL: {web_input.par.url}")
    print(f"   Resolution: {web_input.par.w.eval()} x {web_input.par.h.eval()}")
    print(f"   Audio: {'Enabled' if web_input.par.enableaudio.eval() else 'Disabled'}")
    print(f"   Active: {'Yes' if web_input.par.active.eval() else 'No'}")
    
    return web_input

def find_existing_ndi_out():
    """Find existing NDI Out TOP if it exists"""
    for child in op('/').children:
        if child.type == 'ndioutTOP':
            return child
    return None

def setup_ndi_output():
    """Create or configure NDI Out TOP for sending to OBS"""
    
    print("\n" + "="*60)
    print("SETTING UP NDI OUTPUT")
    print("="*60)
    
    # Check if NDI Out already exists
    existing_ndi = find_existing_ndi_out()
    
    if existing_ndi:
        print(f"\n✅ Found existing NDI Out: {existing_ndi.path}")
        ndi_out = existing_ndi
    else:
        print("\n1. Creating NDI Out TOP...")
        ndi_out = op('/').create(ndioutTOP, 'ndiout_livekit_processed')
        print(f"   ✅ Created: {ndi_out.path}")
        
        # Position it
        ndi_out.nodeX = 200
        ndi_out.nodeY = 200
    
    # Configure it
    print("\n2. Configuring NDI Out TOP...")
    ndi_out.par.active = True
    ndi_out.par.ndiname = 'TD-LiveKit-Output'
    
    print(f"   NDI Name: {ndi_out.par.ndiname}")
    print(f"   Active: {'Yes' if ndi_out.par.active.eval() else 'No'}")
    
    return ndi_out

def create_simple_passthrough(web_input, ndi_out):
    """Create a simple passthrough connection for testing"""
    
    print("\n" + "="*60)
    print("CREATING TEST CONNECTION")
    print("="*60)
    
    print("\n1. Connecting Web Render directly to NDI Out for initial test...")
    
    # Connect web input directly to NDI out
    ndi_out.inputConnectors[0].connect(web_input)
    
    print(f"   ✅ Connected: {web_input.path} → {ndi_out.path}")
    print("\n   This is a direct passthrough for testing.")
    print("   You can insert your processing between these later!")
    
    return True

def display_network_info():
    """Display information about the created network"""
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    web_input = op('/webrender_livekit_input')
    ndi_out = find_existing_ndi_out()
    
    if web_input and ndi_out:
        print("\n✅ WebRTC Receiver Ready:")
        print(f"   Operator: {web_input.path}")
        print(f"   URL: {web_input.par.url}")
        print(f"   Status: {'Active' if web_input.par.active.eval() else 'Inactive'}")
        
        print("\n✅ NDI Output Ready:")
        print(f"   Operator: {ndi_out.path}")
        print(f"   NDI Name: {ndi_out.par.ndiname}")
        print(f"   Status: {'Active' if ndi_out.par.active.eval() else 'Inactive'}")
        
        print("\n📋 Next Steps:")
        print("   1. On your phone, open: http://192.168.24.70:3000/publisher.html")
        print("   2. Click 'Start Publishing' and grant camera permissions")
        print("   3. Watch the webrender_livekit_input operator - you should see your phone!")
        print("   4. The NDI output is available as 'TD-LiveKit-Output'")
        print("   5. In OBS, add NDI Source and select 'TD-LiveKit-Output'")
        print("   6. Test the complete loop!")
        
        print("\n🎨 To Add Your Processing:")
        print("   1. Disconnect NDI Out input")
        print("   2. Insert your effects between Web Render and NDI Out")
        print("   3. Reconnect to NDI Out")
        
        return True
    else:
        print("\n❌ Setup incomplete - check errors above")
        return False

def main():
    """Main execution function"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  TouchDesigner WebRTC/LiveKit Auto-Setup                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Get current state
    print("\n📊 Analyzing current TouchDesigner network...")
    current_ops = get_current_operators()
    print(f"   Found {len(current_ops)} operators in root")
    
    # Setup receiver
    web_input = setup_webrtc_receiver()
    
    # Setup output
    ndi_out = setup_ndi_output()
    
    # Create connection
    create_simple_passthrough(web_input, ndi_out)
    
    # Display info
    display_network_info()
    
    print("\n" + "="*60)
    print("Ready to receive WebRTC streams! 🚀")
    print("="*60 + "\n")

# Execute main function
if __name__ == '__main__':
    main()
