# ULTIMATE TOUCHDESIGNER AUTO-SETUP
# This will find, create, or configure Web Client TOP for LiveKit input
# Run this in TouchDesigner textport (Alt+T)

print("=" * 80)
print("🚀 ULTIMATE TOUCHDESIGNER AUTO-SETUP")
print("=" * 80)

# Configuration
TARGET_URL = "http://localhost:3000/td-input-viewer.html"
TARGET_NAME = "livekit_input"
RESOLUTION_W = 1920
RESOLUTION_H = 1080

# Step 1: Find all existing Web Client TOPs
print("\n📍 STEP 1: Searching for Web Client TOPs...")
all_web_clients = root.findChildren(type='webclientTOP')

if len(all_web_clients) == 0:
    print("  ⚠️  No Web Client TOPs found")
    print("  ✅ Creating new Web Client TOP...")
    web = root.create('webclientTOP', TARGET_NAME)
    print(f"  ✅ Created: {web.path}")
else:
    print(f"  ✅ Found {len(all_web_clients)} Web Client TOP(s)")
    
    # Check if any already have our URL
    existing_with_url = None
    for wc in all_web_clients:
        try:
            url = wc.par.url.eval()
            if TARGET_URL in url:
                existing_with_url = wc
                print(f"  ✅ Found existing with correct URL: {wc.path}")
                break
        except:
            pass
    
    if existing_with_url:
        web = existing_with_url
        print(f"  ✅ Using existing Web Client TOP: {web.path}")
    else:
        # Use the first one
        web = all_web_clients[0]
        print(f"  ✅ Using first Web Client TOP: {web.path}")

# Step 2: Configure all parameters
print("\n🔧 STEP 2: Configuring parameters...")

try:
    # URL
    web.par.url = TARGET_URL
    print(f"  ✅ URL: {web.par.url.eval()}")
    
    # Resolution
    web.par.resolutionw = RESOLUTION_W
    web.par.resolutionh = RESOLUTION_H
    print(f"  ✅ Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
    
    # Audio
    web.par.audio = 'on'
    print(f"  ✅ Audio: {web.par.audio.eval()}")
    
    # Active
    web.par.active = True
    print(f"  ✅ Active: {web.par.active.eval()}")
    
except Exception as e:
    print(f"  ❌ Error configuring: {e}")

# Step 3: Force reload
print("\n🔄 STEP 3: Reloading page...")
try:
    web.par.reload.pulse()
    print("  ✅ Page reload triggered!")
except Exception as e:
    print(f"  ❌ Error reloading: {e}")

# Step 4: Display viewport (if possible)
print("\n👁️  STEP 4: Setting up viewport...")
try:
    web.viewer = True
    print("  ✅ Viewer enabled")
except Exception as e:
    print(f"  ⚠️  Could not enable viewer: {e}")

# Step 5: Verification
print("\n✅ STEP 5: Final verification...")
print(f"  Web Client TOP: {web.path}")
print(f"  URL: {web.par.url.eval()}")
print(f"  Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
print(f"  Audio: {web.par.audio.eval()}")
print(f"  Active: {web.par.active.eval()}")

# Step 6: Instructions
print("\n" + "=" * 80)
print("✅ CONFIGURATION COMPLETE!")
print("=" * 80)
print("\n📋 NEXT STEPS:")
print("\n1. ✅ Web Client TOP configured!")
print(f"   - Name: {web.name}")
print(f"   - Path: {web.path}")
print("\n2. 📹 START THE PUBLISHER:")
print("   - Open Firefox: http://localhost:3000/publisher.html")
print("   - Allow camera access")
print("   - Click 'Start Publishing'")
print("\n3. 👀 CHECK THE WEB CLIENT TOP:")
print("   - You should see video appearing!")
print("   - If not, click the Reload parameter")
print("\n4. 🔍 TROUBLESHOOTING:")
print("   - Status Dashboard: http://localhost:3000/status-dashboard.html")
print("   - Master Test: http://localhost:3000/master-test.html")
print("\n" + "=" * 80)
print("✨ Ready to receive LiveKit video! ✨")
print("=" * 80)

# Return the web client TOP for further use
web
