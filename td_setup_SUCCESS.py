# TouchDesigner WebRTC Setup - ACTUALLY FINAL VERSION
print("="*60)
print("TouchDesigner WebRTC/LiveKit Setup - SUCCESS!")
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

# Configure Web Render TOP - ALL CORRECT PARAMETER NAMES
web.par.url = 'http://localhost:3000/td-auto-viewer.html'
web.par.active = True
web.par.audio = 'on'
web.par.outputresolution = 'custom'
web.par.resolutionw = 1920
web.par.resolutionh = 1080
web.nodeX = -200
web.nodeY = 200

print(f"URL: {web.par.url}")
print(f"Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
print(f"Audio: {web.par.audio.eval()}")
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

# Configure NDI Out - CORRECT: 'name' not 'ndiname'
ndi.par.active = True
ndi.par.name = 'TD-LiveKit-Output'

print(f"NDI Name: {ndi.par.name}")
print(f"Active: {ndi.par.active.eval()}")

# Step 3: Connect them
print("\n" + "="*60)
print("STEP 3: Connecting operators")
print("="*60)

ndi.inputConnectors[0].connect(web)
print(f"✅ Connected: {web.path} → {ndi.path}")

# Done!
print("\n" + "="*60)
print("✅✅✅ SETUP COMPLETE! ✅✅✅")
print("="*60)
print("\n📋 Next Steps:")
print("1. On phone/browser: http://192.168.24.70:3000/publisher.html")
print("2. Click 'Start Publishing'")
print("3. Grant camera permissions")
print("4. Watch webrender_livekit_input - you should see video!")
print("5. In OBS: Add NDI Source → 'TD-LiveKit-Output'")
print("\n🎉 Ready to stream!")
