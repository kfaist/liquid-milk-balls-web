# Quick test to verify TouchDesigner Python environment
print("Testing TouchDesigner operator creation...")

try:
    # Test creating a simple operator
    test_op = op('/').create(constanttop, 'test_webrtc_setup')
    print(f"SUCCESS: Created test operator at {test_op.path}")
    
    # Delete the test operator
    test_op.destroy()
    print("Test operator cleaned up")
    
    print("\nTouchDesigner Python environment is working correctly!")
    print("Ready to create Web Render TOP...")
    
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
