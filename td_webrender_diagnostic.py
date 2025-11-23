"""
TouchDesigner WebRender Diagnostic
Checks the webrender_livekit_input operator configuration and status
"""

import sys

# This script needs to be run from within TouchDesigner's Python environment
# We'll create instructions for manual checking

print("="*60)
print("TOUCHDESIGNER WEBRENDER DIAGNOSTIC")
print("="*60)

print("\nMANUAL CHECKS TO PERFORM IN TOUCHDESIGNER:")

print("\n1. FIND THE WEBRENDER OPERATOR")
print("   - Press Alt+L to open the search dialog")
print("   - Type: webrender_livekit_input")
print("   - Or look for: webrender1, webRenderTOP1, or similar")

print("\n2. CHECK OPERATOR PARAMETERS")
print("   Right-click the operator → Parameters")
print("   Verify these settings:")
print("   - Room Name: claymation-live")
print("   - Server URL: wss://claymation-transcription-l6e51sws.livekit.cloud")
print("   - Token: Should be auto-generated or provided")

print("\n3. CHECK CONNECTION STATUS")
print("   Look at the operator's info panel (bottom right)")
print("   Should show:")
print("   - Connected: Yes")
print("   - Participants: 1 or more")
print("   - Video tracks: 1 or more")

print("\n4. CHECK OUTPUT")
print("   - Click on the webrender operator")
print("   - Look at the viewer window")
print("   - Should show camera feed")

print("\n5. COMMON ISSUES:")
print("   - Black screen = Not connected or no video tracks")
print("   - Error message = Check room name and server URL")
print("   - No operator = Operator not created yet")

print("\n" + "="*60)
print("AUTOMATED CHECKS")
print("="*60)

# Try to detect if we're running inside TouchDesigner
try:
    import td
    print("\n✓ Running inside TouchDesigner environment")
    
    # Try to find webrender operators
    print("\nSearching for WebRender operators...")
    
    all_ops = op('/').findChildren(type=webRenderTOP, depth=10)
    
    if not all_ops:
        print("✗ No WebRender operators found!")
        print("  You need to create a webRenderTOP operator")
    else:
        print(f"✓ Found {len(all_ops)} WebRender operator(s):")
        for operator in all_ops:
            print(f"\n  Operator: {operator.path}")
            print(f"  Active: {operator.par.active.eval()}")
            
            # Check for LiveKit-specific parameters
            if hasattr(operator.par, 'roomname'):
                print(f"  Room Name: {operator.par.roomname.eval()}")
            if hasattr(operator.par, 'serverurl'):
                print(f"  Server URL: {operator.par.serverurl.eval()}")
            
            # Check connection status
            print(f"  Cooking: {operator.isCooking}")
            print(f"  Errors: {operator.errors()}")
            
except ImportError:
    print("\n✗ Not running inside TouchDesigner")
    print("  To use automated checks:")
    print("  1. Open TouchDesigner")
    print("  2. Open Textport (Alt+T)")
    print("  3. Run: run('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_webrender_diagnostic.py')")

print("\n" + "="*60)
print("NEXT STEPS")
print("="*60)

print("\nIf WebRender operator exists but shows black:")
print("1. Check if publisher page is sending camera")
print("2. Verify room name matches: claymation-live")
print("3. Check LiveKit URL is correct")
print("4. Generate a fresh token")

print("\nIf WebRender operator doesn't exist:")
print("1. Create a new webRenderTOP operator")
print("2. Configure it with LiveKit settings")
print("3. Connect it to your effect chain")

print("\n" + "="*60)
