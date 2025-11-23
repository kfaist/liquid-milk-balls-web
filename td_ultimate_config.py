"""
ULTIMATE TOUCHDESIGNER LIVEKIT CONFIGURATOR
Run this INSIDE TouchDesigner textport with:
exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_ultimate_config.py').read())
"""

# LiveKit Configuration
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
ROOM_NAME = "claymation-live"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs"

print("=" * 80)
print("TOUCHDESIGNER LIVEKIT CONFIGURATOR")
print("=" * 80)

# Find or create Web Render TOP
webrender = None

# Search for existing Web Render TOP
print("\nSearching for Web Render TOP operators...")
all_tops = op('/').findChildren(type=baseCOMP)
for top in all_tops:
    if 'webrender' in top.name.lower():
        webrender = top
        print(f"Found existing: {top.path}")
        break

if not webrender:
    print("No Web Render TOP found.")
    print("\nCREATING NEW WEB RENDER TOP...")
    try:
        # Try to create in root
        webrender = op('/').create(baseCOMP, 'webrender_livekit')
        print(f"Created: {webrender.path}")
    except:
        print("Could not create Web Render TOP automatically.")
        print("\nMANUAL CREATION NEEDED:")
        print("1. Press TAB in network editor")
        print("2. Type 'web render'")
        print("3. Press ENTER and click to place")
        print("4. Run this script again")
        print("\nOr provide the operator path:")
        print("webrender = op('/path/to/your/webrender')")

if webrender:
    print(f"\n{'='*80}")
    print(f"CONFIGURING: {webrender.path}")
    print(f"{'='*80}")
    
    # List all parameters
    print("\nAvailable parameters:")
    for par in webrender.pars():
        if any(keyword in par.name.lower() for keyword in ['live', 'kit', 'room', 'token', 'url', 'connect']):
            print(f"  {par.name} = {par.val}")
    
    # Try to set parameters using common parameter names
    configured = []
    
    # Try URL parameters
    for url_param in ['livekiturl', 'url', 'serverurl', 'server', 'wsurl']:
        if hasattr(webrender.par, url_param):
            setattr(webrender.par, url_param, LIVEKIT_URL)
            configured.append(f"✓ Set {url_param} = {LIVEKIT_URL}")
            break
    
    # Try Room parameters
    for room_param in ['roomname', 'room', 'channelname', 'channel']:
        if hasattr(webrender.par, room_param):
            setattr(webrender.par, room_param, ROOM_NAME)
            configured.append(f"✓ Set {room_param} = {ROOM_NAME}")
            break
    
    # Try Token parameters
    for token_param in ['token', 'livekittoken', 'accesstoken', 'auth', 'authtoken']:
        if hasattr(webrender.par, token_param):
            setattr(webrender.par, token_param, TOKEN)
            configured.append(f"✓ Set {token_param} = [TOKEN]")
            break
    
    # Try Enable LiveKit
    for enable_param in ['uselivekit', 'enablelivekit', 'livekitenable', 'enable']:
        if hasattr(webrender.par, enable_param):
            try:
                setattr(webrender.par, enable_param, True)
                configured.append(f"✓ Enabled {enable_param}")
            except:
                setattr(webrender.par, enable_param, 1)
                configured.append(f"✓ Enabled {enable_param}")
            break
    
    # Try Connect
    for connect_param in ['connect', 'start', 'active']:
        if hasattr(webrender.par, connect_param):
            try:
                getattr(webrender.par, connect_param).pulse()
                configured.append(f"✓ Triggered {connect_param}")
            except:
                try:
                    setattr(webrender.par, connect_param, True)
                    configured.append(f"✓ Activated {connect_param}")
                except:
                    pass
            break
    
    print(f"\n{'='*80}")
    print("CONFIGURATION RESULTS:")
    print(f"{'='*80}")
    
    if configured:
        for msg in configured:
            print(msg)
    else:
        print("⚠ Could not auto-configure parameters")
        print("\nMANUAL CONFIGURATION REQUIRED:")
        print(f"  URL:   {LIVEKIT_URL}")
        print(f"  Room:  {ROOM_NAME}")
        print(f"  Token: {TOKEN[:50]}...")
    
    print(f"\n{'='*80}")
    print("NEXT STEPS:")
    print(f"{'='*80}")
    print("1. Check if Web Render TOP shows video")
    print("2. Open publisher.html in browser")
    print("3. Click 'Start Publishing'")
    print("4. Video should appear in TD!")
    print(f"{'='*80}\n")
