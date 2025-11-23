"""
TouchDesigner WebRender TOP Configuration Script
Execute this in TouchDesigner's textport (Alt+T)

This script will:
1. Configure the WebRender TOP at /webrender_livekit_input
2. Set the URL to http://localhost:3000/td-auto-viewer.html
3. Enable media stream access
4. Reload the WebRender TOP
"""

# Get the WebRender TOP
wr = op('/webrender_livekit_input')

print('=' * 80)
print('CONFIGURING WEBRENDER TOP')
print('=' * 80)

# Check if operator exists
if wr is None:
    print('ERROR: WebRender TOP not found at /webrender_livekit_input')
    print('Please verify the operator exists in your project.')
else:
    print(f'WebRender TOP found: {wr}')
    print()
    
    # Step 1: Set the URL
    print('Step 1: Setting URL...')
    target_url = 'http://localhost:3000/td-auto-viewer.html'
    
    # Try different URL parameter names
    url_set = False
    for param_name in ['url', 'Url', 'URL']:
        if hasattr(wr.par, param_name):
            setattr(wr.par, param_name, target_url)
            print(f'  ✓ URL parameter "{param_name}" set to: {target_url}')
            url_set = True
            break
    
    if not url_set:
        print('  ✗ Could not find URL parameter')
    print()
    
    # Step 2: Enable Media Stream
    print('Step 2: Enabling Media Stream...')
    media_enabled = False
    
    # Try various parameter name variations
    media_param_names = [
        'Enablemediastream',
        'enablemediastream', 
        'Enablemedia',
        'enablemedia',
        'Enableaudio',
        'enableaudio',
        'enablemic',
        'Enablemic',
        'enablecamera',
        'Enablecamera'
    ]
    
    for param_name in media_param_names:
        if hasattr(wr.par, param_name):
            param = getattr(wr.par, param_name)
            param.val = 1  # Enable it
            print(f'  ✓ Media parameter "{param_name}" enabled')
            media_enabled = True
    
    if not media_enabled:
        print('  ⚠ Warning: Could not find media stream parameter')
        print('  Listing all parameters to help find the correct one:')
        print()
        print('  ALL WEBRENDER TOP PARAMETERS:')
        for p in wr.pars():
            print(f'    {p.name}: {p.val}')
    print()
    
    # Step 3: Reload the WebRender TOP
    print('Step 3: Reloading WebRender TOP...')
    reload_pulsed = False
    
    for param_name in ['Reload', 'reload', 'Refresh', 'refresh']:
        if hasattr(wr.par, param_name):
            param = getattr(wr.par, param_name)
            param.pulse()
            print(f'  ✓ Reload parameter "{param_name}" pulsed')
            reload_pulsed = True
            break
    
    if not reload_pulsed:
        print('  ⚠ Warning: Could not find reload parameter')
    print()
    
    # Step 4: Verify configuration
    print('=' * 80)
    print('FINAL CONFIGURATION:')
    print('=' * 80)
    
    # Show current URL
    for param_name in ['url', 'Url', 'URL']:
        if hasattr(wr.par, param_name):
            param = getattr(wr.par, param_name)
            print(f'URL ({param_name}): {param.eval()}')
    
    # Show media stream status
    for param_name in media_param_names:
        if hasattr(wr.par, param_name):
            param = getattr(wr.par, param_name)
            print(f'Media Stream ({param_name}): {param.eval()}')
    
    print()
    print('WebRender TOP Size: {}x{}'.format(wr.width, wr.height))
    print('=' * 80)
    print()
    print('NEXT STEPS:')
    print('1. Open http://localhost:3000/publisher.html in a browser')
    print('2. Click "Start Publishing" to send your camera feed')
    print('3. The WebRender TOP should display the incoming video')
    print('=' * 80)
