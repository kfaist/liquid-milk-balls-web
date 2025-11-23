"""
List all operators in TouchDesigner project to see what's already there
"""

import sys

try:
    import td
except ImportError:
    print("ERROR: This must be run from TouchDesigner's Textport")
    print("\nInstructions:")
    print("1. In TouchDesigner, press Alt+T to open Textport")
    print("2. Copy and paste this command:")
    print("   exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/list_td_operators.py').read())")
    sys.exit(1)

print("=" * 60)
print("TOUCHDESIGNER PROJECT ANALYSIS")
print("=" * 60)

# List all TOP operators
print("\n[1] ALL TOP OPERATORS IN PROJECT:")
print("-" * 60)
tops = root.findChildren(type=TOP)
for t in tops:
    print(f"  {t.path:40} | Type: {t.type}")

# Look specifically for WebRender TOPs
print("\n[2] WEBRENDER TOP OPERATORS:")
print("-" * 60)
webrenders = [t for t in tops if 'webrender' in t.type.lower() or 'web' in t.name.lower()]
if webrenders:
    for wr in webrenders:
        print(f"  Name: {wr.name}")
        print(f"  Path: {wr.path}")
        print(f"  Type: {wr.type}")
        print(f"  Active: {wr.par.active if hasattr(wr.par, 'active') else 'N/A'}")
        print(f"  URL: {wr.par.url if hasattr(wr.par, 'url') else 'N/A'}")
        print("-" * 60)
else:
    print("  No WebRender TOPs found")

# Look for NDI operators
print("\n[3] NDI OPERATORS:")
print("-" * 60)
ndi_ops = [op for op in root.findChildren() if 'ndi' in op.name.lower() or 'ndi' in str(op.type).lower()]
if ndi_ops:
    for ndi in ndi_ops:
        print(f"  Name: {ndi.name}")
        print(f"  Path: {ndi.path}")
        print(f"  Type: {ndi.type}")
        if hasattr(ndi.par, 'active'):
            print(f"  Active: {ndi.par.active}")
        if hasattr(ndi.par, 'ndiname'):
            print(f"  NDI Name: {ndi.par.ndiname}")
        print("-" * 60)
else:
    print("  No NDI operators found")

# Look for anything with "livekit" in the name
print("\n[4] LIVEKIT-RELATED OPERATORS:")
print("-" * 60)
livekit_ops = [op for op in root.findChildren() if 'livekit' in op.name.lower()]
if livekit_ops:
    for lk in livekit_ops:
        print(f"  Name: {lk.name}")
        print(f"  Path: {lk.path}")
        print(f"  Type: {lk.type}")
        print("-" * 60)
else:
    print("  No operators with 'livekit' in name")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total TOP operators: {len(tops)}")
print(f"WebRender TOPs: {len(webrenders)}")
print(f"NDI operators: {len(ndi_ops)}")
print(f"LiveKit operators: {len(livekit_ops)}")
