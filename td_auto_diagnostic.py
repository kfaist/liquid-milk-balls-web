# Auto-diagnostic sequence for WebRender video issue
import time

print("=" * 60)
print("AUTOMATED WEBRENDER VIDEO DIAGNOSTIC")
print("=" * 60)

wr1 = op('/project1/webrender1')

# Test 1: Load force video test
print("\n[TEST 1] Loading force_video.html...")
wr1.par.url = 'http://localhost:3000/force_video.html'
wr1.par.reloadsrc.pulse()
print("✓ Loaded - waiting 3 seconds...")

# Can't actually wait in TD script, but will queue the rest
print("\n[TEST 2] Checking TOP output dimensions...")
print(f"  TOP width: {wr1.width}")
print(f"  TOP height: {wr1.height}")
print(f"  Resolution setting: {wr1.par.resolutionw.eval()}x{wr1.par.resolutionh.eval()}")

print("\n[TEST 3] Verifying all settings...")
print(f"  Active: {wr1.par.active.eval()}")
print(f"  Media Stream: {wr1.par.mediastream.eval()}")
print(f"  Always Cook: {wr1.par.alwayscook.eval()}")
print(f"  Max Render Rate: {wr1.par.maxrenderrate.eval()}")

print("\n[TEST 4] Trying different resolutions...")
# Try lower resolution in case rendering issue
wr1.par.resolutionw = 640
wr1.par.resolutionh = 480
wr1.par.reloadsrc.pulse()
print("✓ Set to 640x480, reloaded")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("Take a screenshot of webrender1 output now")
print("=" * 60)
