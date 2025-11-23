"""
TouchDesigner Configuration Script
Run this INSIDE TouchDesigner's textport or a DAT
This will configure WebRTC to receive video from publisher.html
"""

# LiveKit Configuration from Railway
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
ROOM_NAME = "claymation-live"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs"

def configure_webrender():
    """
    Find or create a Web Render TOP and configure it for LiveKit
    """
    print("=" * 60)
    print("TOUCHDESIGNER LIVEKIT WEBRTC CONFIGURATION")
    print("=" * 60)
    
    # Try to find existing Web Render TOP
    webrender = None
    for top in op('/').findChildren(type=webRenderTOP):
        print(f"Found existing Web Render TOP: {top.path}")
        webrender = top
        break
    
    # If not found, try to create one
    if webrender is None:
        print("No Web Render TOP found. Creating one...")
        try:
            # Create in root
            webrender = op('/').create(webRenderTOP, 'webrender_livekit')
            print(f"Created Web Render TOP: {webrender.path}")
        except Exception as e:
            print(f"Error creating Web Render TOP: {e}")
            print("\nMANUAL STEPS REQUIRED:")
            print("1. Create a Web Render TOP operator manually")
            print("2. Name it 'webrender_livekit'")
            print("3. Run this script again")
            return None
    
    # Configure the Web Render TOP
    print(f"\nConfiguring {webrender.path}...")
    
    try:
        # Set LiveKit URL
        if hasattr(webrender.par, 'livekiturl'):
            webrender.par.livekiturl = LIVEKIT_URL
            print(f"✓ Set LiveKit URL: {LIVEKIT_URL}")
        
        # Set Room Name
        if hasattr(webrender.par, 'roomname'):
            webrender.par.roomname = ROOM_NAME
            print(f"✓ Set Room Name: {ROOM_NAME}")
        
        # Set Token
        if hasattr(webrender.par, 'token') or hasattr(webrender.par, 'livekittoken'):
            token_par = 'livekittoken' if hasattr(webrender.par, 'livekittoken') else 'token'
            setattr(webrender.par, token_par, TOKEN)
            print(f"✓ Set Token")
        
        # Enable LiveKit
        if hasattr(webrender.par, 'uselivekit'):
            webrender.par.uselivekit = True
            print(f"✓ Enabled LiveKit mode")
        
        # Try to connect
        if hasattr(webrender.par, 'connect'):
            webrender.par.connect.pulse()
            print(f"✓ Triggered connection")
        
        print("\n" + "=" * 60)
        print("CONFIGURATION COMPLETE!")
        print("=" * 60)
        print("\nCheck the Web Render TOP - video should appear when")
        print("someone uses the publisher page at:")
        print("https://liquid-milk-balls-web-production-2e8c.up.railway.app/publisher.html")
        print("=" * 60)
        
        return webrender
        
    except Exception as e:
        print(f"Error configuring Web Render TOP: {e}")
        print("\nAvailable parameters:")
        for par in webrender.pars():
            if 'live' in par.name.lower() or 'room' in par.name.lower() or 'token' in par.name.lower():
                print(f"  - {par.name}")
        return webrender

# Run the configuration
if __name__ == "__main__":
    configure_webrender()
