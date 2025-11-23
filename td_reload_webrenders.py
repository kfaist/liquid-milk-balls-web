# TouchDesigner WebRender Reload Script
# Save this as a Text DAT and run it, or copy into Textport

print("=" * 60)
print("RELOADING WEBRENDERS")
print("=" * 60)

# The two WebRender TOPs we found
paths = ['/project1/webrender1', '/project1/webrender_livekit_input']

for path in paths:
    try:
        wr = op(path)
        if not wr:
            print(f"\nX {path} - NOT FOUND")
            continue
            
        print(f"\n[{path}]")
        
        # Print current key parameters
        try:
            print(f"  URL: {wr.par.Urlorfile.eval()}")
        except:
            print(f"  URL: (could not read)")
            
        try:
            print(f"  Media Stream Enabled: {wr.par.Enablemediastream.eval()}")
        except:
            print(f"  Media Stream: (could not read)")
        
        # Try to pulse reload
        reloaded = False
        try:
            wr.par.Reloadsource.pulse()
            print(f"  ✓ Pulsed Reloadsource")
            reloaded = True
        except:
            pass
            
        if not reloaded:
            try:
                wr.par.Reloadcurrentpage.pulse()
                print(f"  ✓ Pulsed Reloadcurrentpage")
                reloaded = True
            except:
                pass
        
        if not reloaded:
            # Toggle bypass as fallback
            try:
                orig = wr.bypass
                wr.bypass = True
                wr.bypass = False
                print(f"  ✓ Toggled bypass to force reload")
                reloaded = True
            except Exception as e:
                print(f"  X Could not reload: {e}")
                
    except Exception as e:
        print(f"\nERROR processing {path}: {e}")

print("\n" + "=" * 60)
print("DONE - Check the WebRender outputs and Console for errors")
print("=" * 60)
