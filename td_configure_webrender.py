"""
TouchDesigner WebRender Auto-Configuration
Run this from TouchDesigner's Textport or DAT execute
"""

# Configuration values
ROOM_NAME = "claymation-live"
SERVER_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJzdWIiOiJ0b3VjaGRlc2lnbmVyLXJlY2VpdmVyIiwiaWF0IjoxNzYzODAxODQ5LCJuYmYiOjE3NjM4MDE4NDksImV4cCI6MTc2Mzg4ODI0OX0.7r4VZzzAnbh-On6cw1D2r2kCN84K4QCcorE5-1ZyoA0"

def configure_webrender():
    """Find and configure webrender operator"""
    
    print("Searching for WebRender operators...")
    
    # Search for webRenderTOP operators
    webrender_ops = []
    
    # Try common locations
    search_paths = [
        '/webrender_livekit_input',
        '/webrender1',
        '/webRenderTOP1',
        '/',  # Search from root
    ]
    
    for path in search_paths:
        try:
            if path == '/':
                # Search all webRenderTOP operators from root
                found = op(path).findChildren(type=webRenderTOP, depth=10)
                webrender_ops.extend(found)
            else:
                o = op(path)
                if o and o.type == webRenderTOP:
                    webrender_ops.append(o)
        except:
            pass
    
    # Remove duplicates
    webrender_ops = list(set(webrender_ops))
    
    if not webrender_ops:
        print("ERROR: No WebRender operators found!")
        print("Creating new webRenderTOP operator at /webrender_livekit_input")
        
        # Try to create one
        try:
            parent = op('/')
            new_op = parent.create(webRenderTOP, 'webrender_livekit_input')
            webrender_ops = [new_op]
            print(f"Created new operator: {new_op.path}")
        except Exception as e:
            print(f"Failed to create operator: {e}")
            return False
    
    print(f"Found {len(webrender_ops)} WebRender operator(s)")
    
    # Configure each one
    for webrender in webrender_ops:
        print(f"\nConfiguring: {webrender.path}")
        
        # Set parameters
        try:
            # Room name
            if hasattr(webrender.par, 'roomname'):
                webrender.par.roomname = ROOM_NAME
                print(f"  Set roomname: {ROOM_NAME}")
            elif hasattr(webrender.par, 'room'):
                webrender.par.room = ROOM_NAME
                print(f"  Set room: {ROOM_NAME}")
            
            # Server URL
            if hasattr(webrender.par, 'serverurl'):
                webrender.par.serverurl = SERVER_URL
                print(f"  Set serverurl: {SERVER_URL}")
            elif hasattr(webrender.par, 'server'):
                webrender.par.server = SERVER_URL
                print(f"  Set server: {SERVER_URL}")
            elif hasattr(webrender.par, 'url'):
                webrender.par.url = SERVER_URL
                print(f"  Set url: {SERVER_URL}")
            
            # Token
            if hasattr(webrender.par, 'token'):
                webrender.par.token = TOKEN
                print(f"  Set token: {TOKEN[:50]}...")
            elif hasattr(webrender.par, 'accesstoken'):
                webrender.par.accesstoken = TOKEN
                print(f"  Set accesstoken: {TOKEN[:50]}...")
            
            # Active
            if hasattr(webrender.par, 'active'):
                webrender.par.active = True
                print(f"  Set active: True")
            
            print(f"  Configuration complete!")
            
            # Try to get status
            if hasattr(webrender, 'isConnected'):
                print(f"  Connected: {webrender.isConnected}")
            
        except Exception as e:
            print(f"  Error configuring: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("CONFIGURATION COMPLETE")
    print("="*60)
    print(f"Room: {ROOM_NAME}")
    print(f"Server: {SERVER_URL}")
    print(f"Token: {TOKEN[:50]}...")
    print("\nNext: Make sure publisher.html has camera running")
    print("Then check webrender operator for video feed")
    
    return True

# Run configuration
if __name__ == "__main__":
    configure_webrender()
