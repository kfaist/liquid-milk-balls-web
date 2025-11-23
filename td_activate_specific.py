# ACTIVATE webrender_livekit1 and show video!
print("="*60)
print("ACTIVATING webrender_livekit1")
print("="*60)

# Get the specific operator
webrender = op('/webrender_livekit1')

if not webrender:
    # Try finding it anywhere
    webrender = op('webrender_livekit1')

if webrender:
    print("\nFound:", webrender.path)
    
    # Show current LiveKit settings
    print("\nCurrent LiveKit settings:")
    try:
        if hasattr(webrender.par, 'livekiturl'):
            print(f"  URL: {webrender.par.livekiturl}")
        if hasattr(webrender.par, 'roomname'):
            print(f"  Room: {webrender.par.roomname}")
        if hasattr(webrender.par, 'token'):
            token_val = str(webrender.par.token)
            print(f"  Token: {token_val[:30]}..." if len(token_val) > 30 else f"  Token: {token_val}")
    except:
        pass
    
    print("\nACTIVATING NOW...")
    
    # Try EVERY possible activation method
    activated = False
    
    # Method 1: Connect button
    try:
        if hasattr(webrender.par, 'connect'):
            webrender.par.connect.pulse()
            print("  ✓ Pulsed 'connect'")
            activated = True
    except Exception as e:
        print(f"  connect: {e}")
    
    # Method 2: Active toggle
    try:
        if hasattr(webrender.par, 'active'):
            webrender.par.active = 1
            print("  ✓ Set 'active' = 1")
            activated = True
    except Exception as e:
        print(f"  active: {e}")
    
    # Method 3: Enable
    try:
        if hasattr(webrender.par, 'enable'):
            webrender.par.enable = 1
            print("  ✓ Set 'enable' = 1")
            activated = True
    except Exception as e:
        pass
    
    # Method 4: Display toggle
    try:
        if hasattr(webrender.par, 'display'):
            webrender.par.display = 1
            print("  ✓ Set 'display' = 1")
            activated = True
    except Exception as e:
        pass
    
    if activated:
        print("\n" + "="*60)
        print("ACTIVATION COMPLETE!")
        print("="*60)
        print("\nCheck the viewer window - video should appear now!")
        print("If still black, start publisher in Tab 131")
    else:
        print("\n" + "="*60)
        print("SHOWING ALL PARAMETERS:")
        print("="*60)
        for p in webrender.pars():
            print(f"  {p.name} = {p.val}")
        print("\nTell me which parameters you see!")
else:
    print("ERROR: Could not find webrender_livekit1")
    print("But I see it in your screenshot!")

print("\n" + "="*60)
