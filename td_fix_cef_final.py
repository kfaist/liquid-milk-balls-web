# TouchDesigner CEF Cache Setup - CORRECT PARAMETER NAMES
import os

print("=" * 60)
print("SETTING CEF CACHE & RESTARTING (CORRECT PARAMS)")
print("=" * 60)

# Create cache directory
cache_dir = r"C:/Users/krista-showputer/AppData/Local/TD_cef_cache"
os.makedirs(cache_dir, exist_ok=True)
print(f"✓ Cache directory: {cache_dir}\n")

paths = ['/project1/webrender1', '/project1/webrender_livekit_input']

for path in paths:
    wr = op(path)
    print(f"[{path}]")
    
    # Set user cache directory (correct parameter name: userdir)
    wr.par.userdir = cache_dir
    print(f"  ✓ Set userdir = {cache_dir}")
    
    # Pulse autorestart to restart CEF with new cache
    wr.par.autorestartpulse.pulse()
    print(f"  ✓ Pulsed autorestartpulse (CEF restarting)")
    
    # Also pulse reload to refresh page
    wr.par.reloadsrc.pulse()
    print(f"  ✓ Pulsed reloadsrc (page reloading)")
    print()

print("=" * 60)
print("DONE! CEF restarted with fresh cache")
print("Watch the WebRender outputs for camera video")
print("Check Dialogs → Console for any error messages")
print("=" * 60)
