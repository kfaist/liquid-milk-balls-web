# Comprehensive WebRender Video Test Sequence
# This will try multiple approaches and save results

print("=" * 70)
print("COMPREHENSIVE WEBRENDER VIDEO TEST SEQUENCE")
print("=" * 70)

wr1 = op('/project1/webrender1')
results = []

def test_url(name, url, wait_desc=""):
    print(f"\n[{name}]")
    print(f"  Loading: {url}")
    wr1.par.url = url
    wr1.par.reloadsrc.pulse()
    print(f"  ✓ Loaded")
    print(f"  TOP dimensions: {wr1.width}x{wr1.height}")
    if wait_desc:
        print(f"  {wait_desc}")
    return {
        'name': name,
        'url': url,
        'width': wr1.width,
        'height': wr1.height
    }

# Test 1: Original simple test
results.append(test_url(
    "TEST 1: Simple getUserMedia", 
    "http://localhost:3000/simple_getusermedia.html?autostart=1",
    "Status showed 'Camera started' but no video"
))

# Test 2: Fullscreen test
results.append(test_url(
    "TEST 2: Fullscreen camera",
    "http://localhost:3000/camera_test_fullscreen.html",
    "Should show green text 'Camera active' and video"
))

# Test 3: Force video test
results.append(test_url(
    "TEST 3: Force video with diagnostics",
    "http://localhost:3000/force_video.html",
    "Shows videoWidth/videoHeight in green overlay"
))

# Test 4: Canvas rendering
results.append(test_url(
    "TEST 4: Canvas-based rendering",
    "http://localhost:3000/canvas_video_test.html",
    "Uses canvas.drawImage() instead of video element"
))

# Test 5: Try with different resolution
print(f"\n[TEST 5: Lower resolution]")
print(f"  Changing resolution to 640x480...")
wr1.par.resolutionw = 640
wr1.par.resolutionh = 480
wr1.par.reloadsrc.pulse()
print(f"  ✓ Resolution changed, reloaded")
results.append({
    'name': 'TEST 5: 640x480 resolution',
    'width': wr1.width,
    'height': wr1.height
})

# Test 6: Back to 1280x720
print(f"\n[TEST 6: Standard HD resolution]")
wr1.par.resolutionw = 1280
wr1.par.resolutionh = 720
wr1.par.reloadsrc.pulse()
print(f"  ✓ Back to 1280x720")

print("\n" + "=" * 70)
print("TEST SEQUENCE COMPLETE")
print("=" * 70)
print("\nRESULTS SUMMARY:")
for r in results:
    print(f"  {r['name']}: {r.get('width', 'N/A')}x{r.get('height', 'N/A')}")

print("\nCURRENT STATE:")
print(f"  URL: {wr1.par.url.eval()}")
print(f"  TOP Output: {wr1.width}x{wr1.height}")
print(f"  Media Stream: {wr1.par.mediastream.eval()}")
print(f"  Active: {wr1.par.active.eval()}")

print("\n" + "=" * 70)
print("NEXT: Take screenshots after each test loads")
print("Or let me know if any test shows video!")
print("=" * 70)
