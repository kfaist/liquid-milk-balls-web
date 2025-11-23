"""
Verify and manually configure WebRender TOP
This will save output to a file for inspection
"""
import sys

# Save output to file
output_file = 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrender_config_output.txt'
with open(output_file, 'w') as f:
    original_stdout = sys.stdout
    sys.stdout = f
    
    try:
        # Get WebRender TOP
        wr = op('/webrender_livekit_input')
        
        print("=" * 80)
        print("WEBRENDER TOP CURRENT CONFIGURATION")
        print("=" * 80)
        
        if wr is None:
            print("ERROR: WebRender TOP not found at /webrender_livekit_input")
        else:
            print(f"Operator found: {wr}")
            print(f"Type: {wr.type}")
            print()
            
            # Show current URL
            print("CURRENT URL:")
            try:
                print(f"  wr.par.Url = '{wr.par.Url.eval()}'")
            except Exception as e:
                print(f"  Error reading URL: {e}")
            print()
            
            # List all parameters containing 'url', 'media', 'enable', or 'reload'
            print("RELEVANT PARAMETERS:")
            for p in wr.pars():
                if any(keyword in p.name.lower() for keyword in ['url', 'media', 'enable', 'audio', 'reload', 'refresh']):
                    print(f"  {p.name:30s} = {p.val}")
            print()
            
            # Now configure it correctly
            print("=" * 80)
            print("SETTING NEW CONFIGURATION")
            print("=" * 80)
            
            # Set URL
            target_url = 'http://localhost:3000/td-auto-viewer.html'
            wr.par.Url = target_url
            print(f"Set URL to: {target_url}")
            print(f"Verified URL is now: {wr.par.Url.eval()}")
            print()
            
            # Try to enable media stream
            media_params_found = []
            for param_name in ['Enablemediastream', 'Enablemedia', 'Enableaudio']:
                if hasattr(wr.par, param_name):
                    param = getattr(wr.par, param_name)
                    param.val = 1
                    media_params_found.append(param_name)
                    print(f"Enabled {param_name}: {param.eval()}")
            
            if not media_params_found:
                print("WARNING: No media stream parameters found")
            print()
            
            # Reload
            if hasattr(wr.par, 'Reload'):
                wr.par.Reload.pulse()
                print("Reloaded WebRender TOP")
            else:
                print("WARNING: No Reload parameter found")
            
            print()
            print("=" * 80)
            print("CONFIGURATION COMPLETE")
            print("=" * 80)
            print(f"Final URL: {wr.par.Url.eval()}")
            print(f"WebRender size: {wr.width}x{wr.height}")
            print("=" * 80)
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    sys.stdout = original_stdout

print(f"Configuration complete! Output saved to: {output_file}")
print("Check the file for results.")
