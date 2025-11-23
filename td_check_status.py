"""
Check TouchDesigner operator status
Run this from TouchDesigner's textport
"""

# Check if webrender operator exists
webrender_op = op('/webrender_livekit_input')
if webrender_op:
    print(f"✅ webrender_livekit_input exists")
    print(f"   Active: {webrender_op.par.active.eval()}")
    print(f"   Room: {webrender_op.par.room.eval()}")
else:
    print("❌ webrender_livekit_input NOT FOUND")

# Check if NDI out operator exists
ndi_op = op('/ndiout_livekit2')
if ndi_op:
    print(f"✅ ndiout_livekit2 exists")
    print(f"   Active: {ndi_op.par.active.eval()}")
    print(f"   Sender Name: {ndi_op.par.sendername.eval()}")
else:
    print("❌ ndiout_livekit2 NOT FOUND")

print("\nDone!")
