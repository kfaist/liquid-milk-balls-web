# COMPREHENSIVE TOUCHDESIGNER CONFIGURATION CHECK
print("=" * 80)
print("🔍 TOUCHDESIGNER CONFIGURATION REPORT")
print("=" * 80)

# Check for WebRender TOPs
print("\n📺 WEBRENDER TOPs:")
print("-" * 80)
webrender_tops = root.findChildren(type='webrenderTOP')
print(f"Total found: {len(webrender_tops)}")

if len(webrender_tops) == 0:
    print("❌ NO WEBRENDER TOPs FOUND!")
    print("   Need to create one!")
else:
    for i, wr in enumerate(webrender_tops, 1):
        print(f"\n  WebRender TOP #{i}:")
        print(f"  Name: {wr.name}")
        print(f"  Path: {wr.path}")
        
        try:
            url = wr.par.url.eval()
            active = wr.par.active.eval()
            w = wr.par.resolutionw.eval()
            h = wr.par.resolutionh.eval()
            audio = wr.par.audio.eval()
            
            print(f"  URL: {url}")
            print(f"  Active: {active}")
            print(f"  Resolution: {w} x {h}")
            print(f"  Audio: {audio}")
            
            # Check URL
            if 'td-input-viewer.html' in url:
                print(f"  ✅ CORRECT URL for viewing LiveKit video!")
            elif 'publisher.html' in url:
                print(f"  ❌ WRONG URL - this is for publishing, not viewing!")
                print(f"     Should be: http://localhost:3000/td-input-viewer.html")
            else:
                print(f"  ⚠️  Unknown URL - may not be LiveKit viewer")
                
        except Exception as e:
            print(f"  ❌ Error reading parameters: {e}")

# Check for Web Client TOPs
print("\n\n📄 WEB CLIENT TOPs:")
print("-" * 80)
webclient_tops = root.findChildren(type='webclientTOP')
print(f"Total found: {len(webclient_tops)}")

if len(webclient_tops) > 0:
    print("⚠️  WARNING: Web Client TOPs found!")
    print("   Web Client TOP shows HTTP headers (text), not webpages!")
    print("   You should use WebRender TOP for video!")
    
    for i, wc in enumerate(webclient_tops, 1):
        print(f"\n  Web Client TOP #{i}:")
        print(f"  Name: {wc.name}")
        print(f"  Path: {wc.path}")
        try:
            url = wc.par.url.eval()
            print(f"  URL: {url}")
            if 'localhost:3000' in url or 'td-input' in url or 'livekit' in url:
                print(f"  ⚠️  This should probably be a WebRender TOP instead!")
        except:
            pass

# Summary
print("\n\n" + "=" * 80)
print("📊 SUMMARY")
print("=" * 80)

if len(webrender_tops) == 0:
    print("❌ NO WEBRENDER TOPs - Need to create one!")
    print("   Run: execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_use_webrender.py')")
elif len(webrender_tops) > 0:
    # Check if any have correct URL
    correct_url_found = False
    for wr in webrender_tops:
        try:
            url = wr.par.url.eval()
            if 'td-input-viewer.html' in url:
                correct_url_found = True
                print(f"✅ WebRender TOP found with CORRECT URL!")
                print(f"   Name: {wr.name}")
                print(f"   Path: {wr.path}")
                if wr.par.active.eval():
                    print(f"   ✅ ACTIVE - Should be displaying video!")
                else:
                    print(f"   ❌ NOT ACTIVE - Turn it on!")
                break
        except:
            pass
    
    if not correct_url_found:
        print("⚠️  WebRender TOPs found but none have correct URL")
        print("   Run: execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/fix_webrender_url.py')")

if len(webclient_tops) > 0:
    print(f"\n⚠️  Found {len(webclient_tops)} Web Client TOP(s)")
    print("   Consider deleting these if they're for LiveKit")

print("\n" + "=" * 80)
