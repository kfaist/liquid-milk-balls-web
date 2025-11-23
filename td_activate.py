# Diagnose Web Render TOP and show video
print("=" * 60)
print("WEB RENDER TOP DIAGNOSTIC")
print("=" * 60)

# Find the Web Render TOP
webrender = None
for child in op('/').findChildren(depth=5):
    if 'webrender' in str(child.type).lower():
        webrender = child
        print("\nFound:", child.path)
        break

if webrender:
    print("\nCURRENT PARAMETER VALUES:")
    print("-" * 60)
    
    # Show ALL parameters and their current values
    for p in webrender.pars():
        if any(keyword in p.name.lower() for keyword in ['live', 'kit', 'room', 'token', 'url', 'connect', 'enable', 'active']):
            print(f"{p.name} = {p.val}")
    
    print("\n" + "=" * 60)
    print("ATTEMPTING TO ACTIVATE...")
    print("=" * 60)
    
    # Try different ways to activate
    try:
        # Method 1: Try to pulse connect
        if hasattr(webrender.par, 'connect'):
            webrender.par.connect.pulse()
            print("✓ Pulsed 'connect' button")
    except:
        pass
    
    try:
        # Method 2: Try to set active
        if hasattr(webrender.par, 'active'):
            webrender.par.active = 1
            print("✓ Set 'active' to 1")
    except:
        pass
    
    try:
        # Method 3: Try to enable
        if hasattr(webrender.par, 'enable'):
            webrender.par.enable = 1
            print("✓ Set 'enable' to 1")
    except:
        pass
    
    try:
        # Method 4: Check if there's an init button
        if hasattr(webrender.par, 'init'):
            webrender.par.init.pulse()
            print("✓ Pulsed 'init' button")
    except:
        pass
    
    try:
        # Method 5: Check if there's a start button
        if hasattr(webrender.par, 'start'):
            webrender.par.start.pulse()
            print("✓ Pulsed 'start' button")
    except:
        pass
    
    print("\n" + "=" * 60)
    print("CHECK NOW!")
    print("=" * 60)
    print("Right-click the Web Render TOP → Viewer")
    print("Video should appear now!")
    print("\nIf not, tell me which parameters you see above")
    print("and I'll tell you exactly what to click/set!")
    
else:
    print("\nERROR: No Web Render TOP found!")
    print("Create one: TAB → 'web render' → ENTER")

print("\n" + "=" * 60)
