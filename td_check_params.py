# Find all parameter names for Web Render TOP
web = op('/webrender_livekit_input')

if web:
    print("="*60)
    print("WEB RENDER TOP PARAMETERS")
    print("="*60)
    
    # Print first 50 parameters
    for i, par in enumerate(web.pars()):
        if i > 50:
            break
        print(f"{par.name:30s} = {par.eval()}")
else:
    print("webrender_livekit_input not found!")
