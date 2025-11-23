# Complete WebRender Camera Diagnostic & Fix
print("=" * 60)
print("COMPLETE CAMERA DIAGNOSTIC & FIX SEQUENCE")
print("=" * 60)

# Step 1: Try fullscreen camera test
print("\n[STEP 1] Loading fullscreen camera test...")
wr1 = op('/project1/webrender1')
wr1.par.url = 'http://localhost:3000/camera_test_fullscreen.html'
wr1.par.reloadsrc.pulse()
print("✓ Loaded camera_test_fullscreen.html")

# Step 2: Verify settings
print("\n[STEP 2] Verifying WebRender settings...")
print(f"  Active: {wr1.par.active.eval()}")
print(f"  Media Stream: {wr1.par.mediastream.eval()}")
print(f"  URL: {wr1.par.url.eval()}")
print(f"  Resolution: {wr1.par.resolutionw.eval()}x{wr1.par.resolutionh.eval()}")
print(f"  Cook Always: {wr1.par.alwayscook.eval()}")

# Step 3: Force maximum visibility
print("\n[STEP 3] Maximizing visibility...")
wr1.par.alwayscook = True
wr1.par.maxrenderrate = 60
print("✓ Set alwayscook=True, maxrenderrate=60")

# Step 4: Check if TOP is actually outputting
print("\n[STEP 4] Checking TOP output...")
try:
    width = wr1.width
    height = wr1.height
    print(f"  TOP output size: {width}x{height}")
    if width > 0 and height > 0:
        print("  ✓ TOP is generating output")
    else:
        print("  ✗ TOP output is zero-sized")
except Exception as e:
    print(f"  ✗ Could not check TOP size: {e}")

# Step 5: Try toggling active
print("\n[STEP 5] Toggling active state...")
wr1.par.active = False
wr1.par.active = True
print("✓ Toggled active off/on")

# Step 6: Final reload
print("\n[STEP 6] Final reload...")
wr1.par.reloadsrc.pulse()
print("✓ Reloaded")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("Check webrender1 output now - should show fullscreen camera")
print("If still black, check Dialogs → Console for errors")
print("=" * 60)
