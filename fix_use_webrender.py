# FIX: USE WEBRENDER TOP INSTEAD OF WEBCLIENT TOP
# WebRender TOP is designed for rendering webpages
# Web Client TOP is for HTTP requests and shows text

print("=" * 80)
print("🔧 FIXING TOUCHDESIGNER - USING WEBRENDER TOP")
print("=" * 80)

TARGET_URL = "http://localhost:3000/td-input-viewer.html"
TARGET_NAME = "livekit_webrender_input"

# Step 1: Look for existing WebRender TOPs
print("\n📍 STEP 1: Searching for WebRender TOPs...")
webrender_tops = root.findChildren(type='webrenderTOP')

if len(webrender_tops) == 0:
    print("  ⚠️  No WebRender TOPs found")
    print("  ✅ Creating new WebRender TOP...")
    web = root.create('webrenderTOP', TARGET_NAME)
    print(f"  ✅ Created: {web.path}")
else:
    print(f"  ✅ Found {len(webrender_tops)} WebRender TOP(s)")
    
    # Check if any already configured
    existing = None
    for wr in webrender_tops:
        try:
            url = wr.par.url.eval()
            if TARGET_URL in url:
                existing = wr
                break
        except:
            pass
    
    if existing:
        web = existing
        print(f"  ✅ Using existing: {web.path}")
    else:
        web = webrender_tops[0]
        print(f"  ✅ Using first WebRender TOP: {web.path}")

# Step 2: Configure WebRender TOP parameters
print("\n🔧 STEP 2: Configuring WebRender TOP...")

try:
    # URL
    web.par.url = TARGET_URL
    print(f"  ✅ URL: {TARGET_URL}")
    
    # Resolution
    web.par.resolutionw = 1920
    web.par.resolutionh = 1080
    print(f"  ✅ Resolution: 1920 x 1080")
    
    # Audio
    web.par.audio = 'on'
    print(f"  ✅ Audio: ON")
    
    # Enable mouse/keyboard (not needed but good to have)
    web.par.enablemouse = False
    web.par.enablekeyboard = False
    
except Exception as e:
    print(f"  ❌ Error: {e}")

# Step 3: Reload the page
print("\n🔄 STEP 3: Reloading page...")
try:
    web.par.reload.pulse()
    print("  ✅ Page reload triggered!")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Step 4: Display information
print("\n✅ STEP 4: WebRender TOP Configuration Complete!")
print(f"  Name: {web.name}")
print(f"  Path: {web.path}")
print(f"  URL: {web.par.url.eval()}")
print(f"  Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
print(f"  Audio: {web.par.audio.eval()}")

# Step 5: Delete old Web Client TOP if exists
print("\n🗑️  STEP 5: Cleaning up old Web Client TOPs...")
web_clients = root.findChildren(type='webclientTOP')
for wc in web_clients:
    try:
        url = wc.par.url.eval()
        if 'td-input-viewer' in url or 'localhost:3000' in url:
            print(f"  ⚠️  Found old Web Client TOP: {wc.path}")
            print(f"     (Web Client TOP shows HTTP headers, not webpages)")
            print(f"     You can delete this: {wc.name}")
    except:
        pass

print("\n" + "=" * 80)
print("✅ WEBRENDER TOP IS NOW CONFIGURED!")
print("=" * 80)
print("\n📋 IMPORTANT DIFFERENCES:")
print("   ❌ Web Client TOP = HTTP requests (shows text/headers)")
print("   ✅ WebRender TOP = Renders webpages (shows video)")
print("\n👀 CHECK THE WEBRENDER TOP NOW!")
print("   - Look for the operator named:", web.name)
print("   - You should see video rendering!")
print("\n💡 If still no video:")
print("   1. Click Reload parameter on WebRender TOP")
print("   2. Check publisher is active")
print("   3. Test URL in browser: http://localhost:3000/td-input-viewer.html")
print("\n" + "=" * 80)

# Return the WebRender TOP
web
