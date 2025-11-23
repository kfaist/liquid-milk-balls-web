# VERIFY WEB CLIENT TOP CONFIGURATION
# This checks if a Web Client TOP exists with the correct URL

print("=" * 80)
print("🔍 VERIFYING WEB CLIENT TOP CONFIGURATION")
print("=" * 80)

TARGET_URL = "http://localhost:3000/td-input-viewer.html"

# Find all Web Client TOPs
web_clients = root.findChildren(type='webclientTOP')

if len(web_clients) == 0:
    print("\n❌ NO WEB CLIENT TOPS FOUND!")
    print("   The setup script may not have run.")
    print("   Try running it manually:")
    print("   execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/ultimate_td_setup.py')")
else:
    print(f"\n✅ Found {len(web_clients)} Web Client TOP(s)")
    
    found_configured = False
    
    for i, web in enumerate(web_clients, 1):
        print(f"\n📍 Web Client TOP #{i}")
        print(f"   Name: {web.name}")
        print(f"   Path: {web.path}")
        
        try:
            url = web.par.url.eval()
            print(f"   URL: {url}")
            
            if TARGET_URL in url:
                print("   ✅ CORRECT URL!")
                found_configured = True
                
                # Check other parameters
                w = web.par.resolutionw.eval()
                h = web.par.resolutionh.eval()
                audio = web.par.audio.eval()
                active = web.par.active.eval()
                
                print(f"   Resolution: {w} x {h}")
                print(f"   Audio: {audio}")
                print(f"   Active: {active}")
                
                if w == 1920 and h == 1080:
                    print("   ✅ Resolution correct!")
                if audio == 'on':
                    print("   ✅ Audio enabled!")
                if active:
                    print("   ✅ Active!")
                    
        except Exception as e:
            print(f"   ⚠️  Error reading parameters: {e}")
    
    print("\n" + "=" * 80)
    
    if found_configured:
        print("✅ WEB CLIENT TOP IS CONFIGURED CORRECTLY!")
        print("=" * 80)
        print("\n👀 CHECK THE WEB CLIENT TOP VIEWER NOW!")
        print("   You should see video from the active publisher!")
        print("\n💡 If you don't see video:")
        print("   1. Click the Reload parameter on the Web Client TOP")
        print("   2. Make sure publisher is active: http://localhost:3000/publisher.html")
        print("   3. Check status: node check-room-status.js")
    else:
        print("⚠️  NO WEB CLIENT TOP WITH CORRECT URL FOUND")
        print("=" * 80)
        print("\n🔧 Run the setup script:")
        print("   execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/ultimate_td_setup.py')")

print("\n" + "=" * 80)
