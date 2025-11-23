# Use TouchDesigner Palette System
print("="*60)
print("Creating Operators via Palette System")
print("="*60)

# In TouchDesigner, operators from palette are accessed via special paths
# Let's try using the palette path method

root = op('/')
print(f"Root: {root.path}")
print(f"Root has {len(root.children)} children")

# Method 1: Copy from palette
print("\n1. Attempting to copy Web Render from palette...")
try:
    # Palette path for Web Render TOP
    palette_web = op('/sys/palette/TOP/webRender')
    if palette_web:
        web = palette_web.copy(root)
        web.name = 'webrender_livekit_input'
        print(f"✅ Copied from palette: {web.path}")
    else:
        print("❌ Palette path not found")
        web = None
except Exception as e:
    print(f"❌ Palette copy failed: {e}")
    web = None

# Method 2: Try alternative palette paths
if not web:
    print("\n2. Trying alternative palette paths...")
    palette_paths = [
        '/palette/TOP/webRender',
        '/Palette/TOP/webRender',  
        '/sys/Palette/TOP/webRender'
    ]
    
    for path in palette_paths:
        try:
            palette_op = op(path)
            if palette_op:
                web = palette_op.copy(root)
                web.name = 'webrender_livekit_input'
                print(f"✅ Found at {path}: {web.path}")
                break
        except:
            continue

# Method 3: Just create a CHOP and we'll verify the syntax
if not web:
    print("\n3. Testing basic operator creation...")
    try:
        # We know constantTOP works, let's verify the pattern
        test = root.create('constantTOP', 'test_verify_syntax')
        print(f"✅ Can create operators: {test.path}")
        print(f"   Operator type: {test.type}")
        
        # Now try variations for webrender
        for variant in ['webRenderTOP', 'webrendertop', 'webrenderTOP']:
            try:
                web = root.create(variant, 'webrender_livekit_input')
                print(f"✅ SUCCESS with {variant}: {web.path}")
                test.destroy()
                break
            except:
                print(f"   ❌ {variant} didn't work")
        
        if not web:
            test.destroy()
    except Exception as e:
        print(f"❌ Basic creation failed: {e}")

if web:
    print(f"\n✅ FINAL: Have Web Render at {web.path}")
    # Configure it
    web.par.url = 'http://localhost:3000/td-auto-viewer.html'
    web.par.w = 1920
    web.par.h = 1080  
    web.par.enableaudio = 1
    web.par.active = 1
    web.nodeX = -200
    web.nodeY = 200
    print("✅ Configured successfully!")
else:
    print("\n❌ Could not create Web Render TOP - trying manual instructions...")

print("\n" + "="*60)
