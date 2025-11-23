# FIX WEBRENDER TOP URL
# The WebRender TOP is working but pointing to the wrong page
# Need to change from publisher.html to td-input-viewer.html

print("=" * 80)
print("🔧 FIXING WEBRENDER TOP URL")
print("=" * 80)

CORRECT_URL = "http://localhost:3000/td-input-viewer.html"

# Find WebRender TOPs
print("\n📍 Finding WebRender TOPs...")
webrender_tops = root.findChildren(type='webrenderTOP')

if len(webrender_tops) == 0:
    print("❌ No WebRender TOPs found!")
    print("   Run: execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_use_webrender.py')")
else:
    print(f"✅ Found {len(webrender_tops)} WebRender TOP(s)")
    
    for web in webrender_tops:
        print(f"\n🔧 Configuring: {web.path}")
        
        # Show current URL
        try:
            current_url = web.par.url.eval()
            print(f"   Current URL: {current_url}")
        except:
            print("   Current URL: [Error reading]")
        
        # Set correct URL
        web.par.url = CORRECT_URL
        print(f"   ✅ New URL: {CORRECT_URL}")
        
        # Reload page
        web.par.reload.pulse()
        print("   ✅ Page reloaded")
        
        print(f"\n   OPERATOR: {web.name}")
        print(f"   PATH: {web.path}")

print("\n" + "=" * 80)
print("✅ URL FIXED!")
print("=" * 80)
print("\n📋 WHAT CHANGED:")
print("   BEFORE: publisher.html (for remote cameras)")
print("   AFTER:  td-input-viewer.html (for viewing in TouchDesigner)")
print("\n👀 CHECK WEBRENDER TOP NOW!")
print("   You should see video from the active publisher!")
print("\n💡 The page should auto-connect to LiveKit and display video")
print("=" * 80)
