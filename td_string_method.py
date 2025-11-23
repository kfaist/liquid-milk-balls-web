# Alternative approach: Use string-based operator creation
print("="*60)
print("TouchDesigner WebRTC Setup - String Method")
print("="*60)

# Method 1: Try using string type names
print("\nAttempt 1: Creating Web Render TOP using string...")
try:
    web = op('/').create('webrendertop', 'webrender_livekit_input')
    print(f"✅ SUCCESS: Created {web.path}")
    web.par.url = 'http://localhost:3000/td-auto-viewer.html'
    web.par.w = 1920
    web.par.h = 1080
    web.par.enableaudio = True
    web.par.active = True
    web.nodeX = -200
    web.nodeY = 200
    print(f"   Configured: {web.par.url}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {e}")
    web = None

# Try NDI Out
print("\nAttempt 2: Creating NDI Out TOP using string...")
try:
    ndi = op('/').create('ndioutTOP', 'ndiout_livekit')
    print(f"✅ SUCCESS: Created {ndi.path}")
    ndi.par.active = True
    ndi.par.ndiname = 'TD-LiveKit-Output'
    ndi.nodeX = 200
    ndi.nodeY = 200
    print(f"   NDI Name: {ndi.par.ndiname}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {e}")
    ndi = None

# Try connecting if both worked
if web and ndi:
    print("\nAttempt 3: Connecting operators...")
    try:
        ndi.inputConnectors[0].connect(web)
        print(f"✅ SUCCESS: Connected {web.path} → {ndi.path}")
        print("\n🎉 COMPLETE! Ready to receive WebRTC streams!")
    except Exception as e:
        print(f"❌ Connection FAILED: {type(e).__name__}: {e}")

print("\n" + "="*60)
