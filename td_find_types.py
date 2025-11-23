# Test 1: Check what operator types are available in TouchDesigner
print("Testing operator type names...")

# List all TOP types we might need
test_types = [
    'webrendertop',
    'webRenderTOP', 
    'WebRenderTOP',
    'webrenderTOP',
    'ndioutTOP',
    'ndioutTop',
    'constanttop',
    'constantTOP'
]

print("\nTesting which operator types exist:")
for type_name in test_types:
    try:
        test = op('/').create(eval(type_name), f'test_{type_name}')
        print(f"✅ {type_name} - EXISTS")
        test.destroy()
    except NameError:
        print(f"❌ {type_name} - NameError")
    except Exception as e:
        print(f"⚠️  {type_name} - {type(e).__name__}: {e}")

print("\nTest complete!")
