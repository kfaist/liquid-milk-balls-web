# Verification script with file output
import json
import os

output_file = 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verification_result.json'

try:
    result = {
        "timestamp": str(op('/').time.frame),
        "webrender_exists": False,
        "ndiout_exists": False,
        "error": None
    }
    
    # Check web render
    web = op('/webrender_livekit_input')
    if web:
        result["webrender_exists"] = True
        result["webrender_details"] = {
            "path": web.path,
            "url": web.par.url.eval(),
            "active": web.par.active.eval(),
            "width": web.par.w.eval(),
            "height": web.par.h.eval()
        }
    
    # Check NDI out
    ndi = op('/ndiout_livekit')
    if ndi:
        result["ndiout_exists"] = True
        result["ndi_details"] = {
            "path": ndi.path,
            "name": ndi.par.ndiname.eval(),
            "active": ndi.par.active.eval(),
            "connected": ndi.inputConnectors[0].connections[0].owner.name if ndi.inputConnectors[0].connections else "NOT_CONNECTED"
        }
    
    result["status"] = "SUCCESS" if (result["webrender_exists"] and result["ndiout_exists"]) else "INCOMPLETE"
    
except Exception as e:
    result = {
        "status": "ERROR",
        "error": str(e)
    }

# Write to file
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)

print(f"Verification written to: {output_file}")
print(json.dumps(result, indent=2))
