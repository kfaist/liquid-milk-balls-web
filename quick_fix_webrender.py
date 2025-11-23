"""
FINAL WebRender TOP Configuration - Direct Parameter Setting
Run this in TouchDesigner's textport
"""

# Get the WebRender TOP
wr = op('/webrender_livekit_input')

print("=" * 80)
print("DIRECT WEBRENDER TOP CONFIGURATION")
print("=" * 80)

if wr is None:
    print("ERROR: WebRender TOP not found!")
else:
    # Set URL
    wr.par.Url = 'http://localhost:3000/td-auto-viewer.html'
    print(f"URL set to: {wr.par.Url}")
    
    # Enable media stream - try all possible parameter names
    try:
        wr.par.Enablemediastream = 1
        print(f"Enablemediastream set to: {wr.par.Enablemediastream}")
    except:
        print("Enablemediastream parameter not found")
    
    try:
        wr.par.Enablemedia = 1
        print(f"Enablemedia set to: {wr.par.Enablemedia}")
    except:
        print("Enablemedia parameter not found")
    
    try:
        wr.par.Enableaudio = 1
        print(f"Enableaudio set to: {wr.par.Enableaudio}")
    except:
        print("Enableaudio parameter not found")
    
    # Reload the page
    try:
        wr.par.Reload.pulse()
        print("Reload pulsed")
    except:
        print("Reload parameter not found")
    
    print("=" * 80)
    print("Configuration complete!")
    print("=" * 80)
    print(f"Current URL: {wr.par.Url}")
    print(f"WebRender size: {wr.width}x{wr.height}")
    print("=" * 80)
