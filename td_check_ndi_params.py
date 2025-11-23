# Find all parameter names for NDI Out TOP
ndi = op('/ndiout_livekit')

if ndi:
    print("="*60)
    print("NDI OUT TOP PARAMETERS")
    print("="*60)
    
    # Print first 30 parameters
    for i, par in enumerate(ndi.pars()):
        if i > 30:
            break
        print(f"{par.name:30s} = {par.eval()}")
else:
    print("ndiout_livekit not found!")
