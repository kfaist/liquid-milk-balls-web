# FINAL COMPREHENSIVE FIX FOR WEBRENDER TOP
# This ensures everything is set up correctly

print("=" * 80)
print("🚀 FINAL COMPREHENSIVE WEBRENDER TOP SETUP")
print("=" * 80)

CORRECT_URL = "http://localhost:3000/td-input-viewer.html"
TARGET_NAME = "livekit_input_viewer"

# Step 1: Check for existing WebRender TOPs
print("\n📍 STEP 1: Checking existing WebRender TOPs...")
webrender_tops = root.findChildren(type='webrenderTOP')

if len(webrender_tops) == 0:
    print("  No WebRender TOPs found")
    print("  Creating new WebRender TOP...")
    web = root.create('webrenderTOP', TARGET_NAME)
    print(f"  ✅ Created: {web.path}")
else:
    print(f"  Found {len(webrender_tops)} existing WebRender TOP(s)")
    
    # Try to find one with our URL or use first one
    web = None
    for wr in webrender_tops:
        try:
            url = wr.par.url.eval()
            if 'td-input-viewer' in url or 'localhost:3000' in url:
                web = wr
                print(f"  ✅ Found existing with LiveKit URL: {wr.path}")
                break
        except:
            pass
    
    if not web:
        web = webrender_tops[0]
        print(f"  ✅ Using first WebRender TOP: {web.path}")

# Step 2: Configure all parameters
print("\n🔧 STEP 2: Configuring WebRender TOP parameters...")

try:
    # URL - MOST IMPORTANT!
    old_url = web.par.url.eval()
    web.par.url = CORRECT_URL
    print(f"  URL:")
    print(f"    Old: {old_url}")
    print(f"    New: {CORRECT_URL}")
    if 'td-input-viewer' in CORRECT_URL:
        print(f"    ✅ CORRECT - This is the viewer page!")
    
    # Resolution
    web.par.resolutionw = 1920
    web.par.resolutionh = 1080
    print(f"  ✅ Resolution: 1920 x 1080")
    
    # Audio
    web.par.audio = 'on'
    print(f"  ✅ Audio: ON")
    
    # Make sure it's active (Cook Always should be On)
    web.par.cookalways = True
    print(f"  ✅ Cook Always: ON")
    
    # Enable Media Stream (important for WebRTC)
    web.par.enablemediastream = True
    print(f"  ✅ Enable Media Stream: ON")
    
except Exception as e:
    print(f"  ❌ Error configuring: {e}")

# Step 3: Reload the page
print("\n🔄 STEP 3: Reloading page...")
try:
    web.par.reload.pulse()
    print("  ✅ Page reload triggered!")
    print("  ⏳ Page is loading...")
except Exception as e:
    print(f"  ❌ Error reloading: {e}")

# Step 4: Summary
print("\n" + "=" * 80)
print("✅ WEBRENDER TOP CONFIGURED!")
print("=" * 80)

print(f"\n📋 Configuration Summary:")
print(f"  Operator: {web.name}")
print(f"  Path: {web.path}")
print(f"  URL: {web.par.url.eval()}")
print(f"  Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
print(f"  Audio: {web.par.audio.eval()}")
print(f"  Cook Always: {web.par.cookalways.eval()}")
print(f"  Enable Media Stream: {web.par.enablemediastream.eval()}")

print(f"\n👀 WHAT TO CHECK NOW:")
print(f"  1. Look at the WebRender TOP viewer")
print(f"  2. You should see full-screen video")
print(f"  3. Video should be updating in real-time")
print(f"  4. If you see 'Connecting...' wait a few seconds")
print(f"  5. If still no video, click Reload parameter")

print(f"\n💡 TROUBLESHOOTING:")
print(f"  • Black screen = Page loading or no publisher")
print(f"  • 'Connecting...' = LiveKit connecting (normal)")
print(f"  • Video visible = SUCCESS!")
print(f"  • Publisher controls = Wrong URL (should be td-input-viewer.html)")

print(f"\n🔗 TEST IN BROWSER:")
print(f"  Open: {CORRECT_URL}")
print(f"  Should see video immediately")
print(f"  If yes in browser but not TD = Click Reload in TD")

print("\n" + "=" * 80)
print("✨ Setup complete! Check the WebRender TOP! ✨")
print("=" * 80)

# Return the WebRender TOP for inspection
web
