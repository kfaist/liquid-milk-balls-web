"""
TouchDesigner WebRTC Operator Diagnostic
Run this INSIDE TouchDesigner to see all WebRTC-related operators and their parameters
"""

def diagnose_webrtc_operators():
    """
    Find all WebRTC-related operators and list their parameters
    """
    print("=" * 80)
    print("TOUCHDESIGNER WEBRTC OPERATOR DIAGNOSTIC")
    print("=" * 80)
    
    # Types to search for
    operator_types = ['webRenderTOP', 'webRTC', 'web']
    found_operators = []
    
    # Search entire project
    print("\nSearching for WebRTC-related operators...")
    
    all_ops = op('/').findChildren(depth=10)
    for o in all_ops:
        op_type = o.type
        if any(keyword.lower() in str(op_type).lower() for keyword in operator_types):
            found_operators.append(o)
            print(f"\nFound: {o.path} (Type: {op_type})")
    
    if not found_operators:
        print("\nNo WebRTC operators found!")
        print("\nTO CREATE A WEB RENDER TOP:")
        print("1. Press TAB in the network editor")
        print("2. Type 'web' to filter")
        print("3. Select 'Web Render TOP'")
        print("4. Place it in your network")
        print("5. Run this script again")
        return
    
    # Examine each operator's parameters
    print("\n" + "=" * 80)
    print("OPERATOR PARAMETERS")
    print("=" * 80)
    
    for op_obj in found_operators:
        print(f"\n{'='*80}")
        print(f"Operator: {op_obj.path}")
        print(f"Type: {op_obj.type}")
        print(f"{'='*80}")
        
        # List ALL parameters
        print("\nALL PARAMETERS:")
        for par in op_obj.pars():
            print(f"  {par.name:<30} = {par.val}")
        
        # Highlight LiveKit/WebRTC related parameters
        print("\nLIVEKIT/WEBRTC RELATED PARAMETERS:")
        relevant_keywords = ['live', 'kit', 'web', 'rtc', 'room', 'token', 'url', 'connect', 'stream']
        found_relevant = False
        
        for par in op_obj.pars():
            if any(keyword in par.name.lower() for keyword in relevant_keywords):
                found_relevant = True
                print(f"  {par.name:<30} = {par.val}")
        
        if not found_relevant:
            print("  (No LiveKit-specific parameters found)")
    
    print("\n" + "=" * 80)
    print("CONFIGURATION INSTRUCTIONS")
    print("=" * 80)
    print("\nLiveKit Connection Details:")
    print(f"  URL:   wss://claymation-transcription-l6e51sws.livekit.cloud")
    print(f"  Room:  claymation-live")
    print(f"  Token: eyJhbGciOiJIUzI1NiJ9...")
    print("\nUse the parameter names listed above to configure your operator")
    print("=" * 80)

# Run diagnostic
if __name__ == "__main__":
    diagnose_webrtc_operators()
