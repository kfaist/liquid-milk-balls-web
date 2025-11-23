# Direct OP creation using parent.create with OP class
print("="*60)
print("Creating Web Render TOP - Direct Method")
print("="*60)

# Get the root
root = op('/')
print(f"Working in: {root.path}")

# List available operator families
print("\nChecking what we can create...")

# Try creating using parent's create method with proper OP family
print("\n1. Creating Web Render TOP...")

# Method: parent.create(family, basename)
# The family for Web Render is typically 'webrender'
try:
    web = root.create(baseCOMP, 'webrender_livekit_input')
    print(f"Attempt 1 - baseCOMP: {web}")
except:
    try:
        web = root.create('webrender', 'webrender_livekit_input')
        print(f"Attempt 2 - 'webrender': {web}")
    except:
        # Last resort - check all children for existing web render
        print("Trying to find existing Web Render TOP...")
        web = None
        for child in root.children:
            print(f"  Found: {child.name} (type: {child.type})")
            if 'web' in child.type.lower() and 'render' in child.type.lower():
                web = child
                print(f"  Using existing: {web.path}")
                break

if web:
    print(f"\n✅ Have Web Render TOP: {web.path}")
    # Configure it
    try:
        web.par.url = 'http://localhost:3000/td-auto-viewer.html'
        web.par.w = 1920
        web.par.h = 1080
        web.par.enableaudio = True
        web.par.active = True
        print("✅ Configured Web Render TOP")
    except Exception as e:
        print(f"⚠️  Configuration error: {e}")
else:
    print("❌ Could not create or find Web Render TOP")

print("\n" + "="*60)
