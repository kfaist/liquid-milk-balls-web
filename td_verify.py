# Quick verification script
import json

result = {
    "webrender_exists": op('/webrender_livekit_input') is not None,
    "ndiout_exists": op('/ndiout_livekit') is not None
}

if result["webrender_exists"]:
    web = op('/webrender_livekit_input')
    result["webrender_url"] = web.par.url.eval()
    result["webrender_active"] = web.par.active.eval()
    
if result["ndiout_exists"]:
    ndi = op('/ndiout_livekit')
    result["ndi_name"] = ndi.par.ndiname.eval()
    result["ndi_active"] = ndi.par.active.eval()
    result["ndi_connected"] = ndi.inputConnectors[0].connections[0].owner.name if ndi.inputConnectors[0].connections else None

print("VERIFICATION_RESULT:")
print(json.dumps(result, indent=2))
