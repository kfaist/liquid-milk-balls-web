# TouchDesigner CEF Cache Setup & Restart
# This often fixes getUserMedia permission issues

import os

print("=" * 60)
print("SETTING UP CEF CACHE & RESTARTING WEBRENDERS")
print("=" * 60)

# Create dedicated cache directory
cache_dir = r"C:/Users/krista-showputer/AppData/Local/TD_cef_cache"
print(f"\nCreating cache directory: {cache_dir}")
os.makedirs(cache_dir, exist_ok=True)
print("✓ Cache directory ready")

# Configure both WebRender TOPs
paths = ['/project1/webrender1', '/project1/webrender_livekit_input']

for path in paths:
    try:
        wr = op(path)
        if not wr:
            print(f"\n✗ {path} - NOT FOUND")
            continue
            
        print(f"\n[{path}]")
        
        # Set cache directory
        try:
            wr.par.Usercachedirectory = cache_dir
            print(f"  ✓ Set cache directory")
        except Exception as e:
            print(f"  ✗ Could not set cache: {e}")
        
        # Enable restart if process died
        try:
            wr.par.Restartifprocessdied = 1
            print(f"  ✓ Enabled restart-if-died")
        except Exception as e:
            print(f"  ⚠ Could not enable restart-if-died: {e}")
        
        # Pulse restart to force CEF reload with new cache
        try:
            wr.par.Restart.pulse()
            print(f"  ✓ Pulsed RESTART (CEF will reload)")
        except Exception as e:
            print(f"  ⚠ No restart parameter: {e}")
            # Try reload as fallback
            try:
                wr.par.Reloadsource.pulse()
                print(f"  ✓ Pulsed reload as fallback")
            except:
                pass
                
    except Exception as e:
        print(f"\n✗ ERROR processing {path}: {e}")

print("\n" + "=" * 60)
print("DONE - WebRenders restarting with fresh CEF cache")
print("Now check Dialogs → Console for any errors")
print("=" * 60)
