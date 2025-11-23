# TouchDesigner WebRTC Setup - WORKING VERSION
print("="*60)
print("TouchDesigner WebRTC/LiveKit Setup - WORKING")
print("="*60)

root = op('/')
print(f"\nWorking in: {root.path}")
print(f"Current children: {len(root.children)}")

# Step 1: Create Web Render TOP
print("\n" + "="*60)
print("STEP 1: Creating Web Render TOP")
print("="*60)

# Check if it exists and remove it
if op('/webrender_livekit_input'):
    old_web = op('/webrender_livekit_input')
    print(f"Found existing: {old_web.path} - removing...")
    old_web.destroy()

# Create with correct syntax
web = root.create(webrenderTOP, 'webrender_livekit_input')
print(f"✅ Created: {web.path}")

# Configure Web Render TOP - Using COMMON page parameters
web.par.url = 'http://localhost:3000/td-auto-viewer.html'
web.par.enableaudio = True
web.par.active = True
web.nodeX = -200
web.nodeY = 200

# The resolution is set on the common page
# First set resolution mode to custom
web.par.res = 'custom'  # Set to custom resolution mode
web.par.w = 1920        # Width on common page
web.par.h = 1080        # Height on common page

print(f"URL: {web.par.url}")
print(f"Resolution: {web.par.w.eval()} x {web.par.h.eval()}")
print(f"Audio: {web.par.enableaudio.eval()}")
print(f"Active: {web.par.active.eval()}")

# Step 2: Find or create NDI Out
print("\n" + "="*60)
print("STEP 2: Setting up NDI Out")
print("="*60)

# Look for existing NDI Out
ndi = None
for child in root.children:
    if child.type == 'ndioutTOP':
        ndi = child
        print(f"Found existing NDI Out: {ndi.path}")
        break

if not ndi:
    ndi = root.create(ndioutTOP, 'ndiout_livekit')
    ndi.nodeX = 200
    ndi.nodeY = 200
    print(f"✅ Created: {ndi.path}")

# Configure NDI Out
ndi.par.active = True
ndi.par.ndiname = 'TD-LiveKit-Output'

print(f"NDI Name: {ndi.par.ndiname}")
print(f"Active: {ndi.par.active.eval()}")

# Step 3: Connect them
print("\n" + "="*60)
print("STEP 3: Connecting operators")
print("="*60)

ndi.inputConnectors[0].connect(web)
print(f"✅ Connected: {web.path} → {ndi.path}")

# Done!
print("\n" + "="*60)
print("SETUP COMPLETE!")
print("="*60)
print("\n📋 Next Steps:")
print("1. On phone/browser: http://192.168.24.70:3000/publisher.html")
print("2. Click 'Start Publishing'")
print("3. Grant camera permissions")
print("4. Watch webrender_livekit_input - you should see video!")
print("5. In OBS: Add NDI Source → 'TD-LiveKit-Output'")
print("\n🎉 Ready to stream!")
