# TouchDesigner WebRTC Setup - Simple Manual Steps
# Copy each section below into the Textport one at a time

print("="*60)
print("STEP 1: Creating Web Render TOP")
print("="*60)

# Create Web Render TOP
web = op('/').create(webrenderTOP, 'webrender_livekit_input')
print(f"Created: {web.path}")

# Configure it
web.par.url = 'http://localhost:3000/td-auto-viewer.html'
web.par.w = 1920
web.par.h = 1080
web.par.enableaudio = True
web.par.active = True

# Position it
web.nodeX = -200
web.nodeY = 200

print(f"URL: {web.par.url}")
print(f"Resolution: {web.par.w.eval()} x {web.par.h.eval()}")
print(f"Audio Enabled: {web.par.enableaudio.eval()}")
print(f"Active: {web.par.active.eval()}")
print("✅ Web Render TOP ready!")

print("\n" + "="*60)
print("STEP 2: Setting up NDI Out")
print("="*60)

# Check if NDI Out already exists
existing_ndi = None
for child in op('/').children:
    if child.type == 'ndioutTOP':
        existing_ndi = child
        break

if existing_ndi:
    print(f"Found existing NDI Out: {existing_ndi.path}")
    ndi = existing_ndi
else:
    ndi = op('/').create(ndioutTOP, 'ndiout_livekit')
    ndi.nodeX = 200
    ndi.nodeY = 200
    print(f"Created: {ndi.path}")

# Configure NDI Out
ndi.par.active = True
ndi.par.ndiname = 'TD-LiveKit-Output'

print(f"NDI Name: {ndi.par.ndiname}")
print(f"Active: {ndi.par.active.eval()}")
print("✅ NDI Out ready!")

print("\n" + "="*60)
print("STEP 3: Connecting Web Render to NDI Out")
print("="*60)

# Connect them
ndi.inputConnectors[0].connect(web)
print(f"✅ Connected: {web.path} → {ndi.path}")

print("\n" + "="*60)
print("SETUP COMPLETE!")
print("="*60)
print("\nNext Steps:")
print("1. Open on phone: http://192.168.24.70:3000/publisher.html")
print("2. Click 'Start Publishing'")
print("3. Watch webrender_livekit_input - you should see your camera!")
print("4. In OBS, add NDI Source: 'TD-LiveKit-Output'")
print("\n🎉 Ready to stream!")
