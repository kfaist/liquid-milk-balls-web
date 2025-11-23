webrender = None
for child in op('/').findChildren(depth=5):
    if 'webrender' in str(child.type).lower():
        webrender = child
        print("Found Web Render TOP:", child.path)
        break

if webrender:
    print("\nShowing LiveKit parameters:")
    for p in webrender.pars():
        if 'live' in p.name.lower() or 'room' in p.name.lower() or 'token' in p.name.lower() or 'url' in p.name.lower() or 'connect' in p.name.lower() or 'active' in p.name.lower():
            print(f"  {p.name} = {p.val}")
    
    print("\nTrying to activate...")
    try:
        if hasattr(webrender.par, 'connect'):
            webrender.par.connect.pulse()
            print("  Pulsed connect button")
    except:
        pass
    
    try:
        if hasattr(webrender.par, 'active'):
            webrender.par.active = 1
            print("  Set active = 1")
    except:
        pass
    
    print("\nDONE! Now right-click the Web Render TOP and select Viewer")
    print("Video should appear!")
else:
    print("ERROR: No Web Render TOP found")
    print("Create one: TAB -> type 'web render' -> ENTER")
