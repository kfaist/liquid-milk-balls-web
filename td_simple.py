# TouchDesigner LiveKit Configuration
# Simple, clean version with NO syntax issues

print("Starting configuration...")

# LiveKit settings
url = "wss://claymation-transcription-l6e51sws.livekit.cloud"
room = "claymation-live"  
token = "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs"

# Find Web Render TOP
webrender = None
for child in op('/').findChildren(depth=5):
    if 'webrender' in str(child.type).lower():
        webrender = child
        print("Found Web Render TOP:", child.path)
        break

if not webrender:
    print("No Web Render TOP found - creating one...")
    try:
        webrender = op('/').create(baseCOMP, 'webrender_livekit')
        print("Created:", webrender.path)
    except:
        print("ERROR: Could not create Web Render TOP")
        print("Please create manually: TAB -> 'web render' -> ENTER")

if webrender:
    print("\nConfiguring Web Render TOP...")
    
    # Try to set parameters
    try:
        # List all parameters
        print("\nAvailable parameters:")
        for p in webrender.pars():
            print("  -", p.name)
        
        # Try common parameter names
        if hasattr(webrender.par, 'livekiturl'):
            webrender.par.livekiturl = url
            print("Set livekiturl")
        
        if hasattr(webrender.par, 'roomname'):
            webrender.par.roomname = room
            print("Set roomname")
            
        if hasattr(webrender.par, 'token'):
            webrender.par.token = token
            print("Set token")
            
        if hasattr(webrender.par, 'uselivekit'):
            webrender.par.uselivekit = 1
            print("Enabled LiveKit")
            
        print("\nConfiguration complete!")
        print("Check the Web Render TOP for video")
        
    except Exception as e:
        print("Error:", str(e))
        print("\nManual configuration needed:")
        print("URL:", url)
        print("Room:", room)
        print("Token:", token[:50], "...")

print("\nDone!")
