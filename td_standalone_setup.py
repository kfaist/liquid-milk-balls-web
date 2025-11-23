# TouchDesigner Setup Script - Put this in a Text DAT and execute it
# Or run via: op('/').create(textDAT, 'setup_script').text = open('this_file.py').read(); exec(op('/setup_script').text)

root = op('/')

# Clean up any existing operators
if op('/webrender_livekit_input'):
    op('/webrender_livekit_input').destroy()
    
if op('/ndiout_livekit'):
    op('/ndiout_livekit').destroy()

# Create Web Render TOP
web = root.create(webrenderTOP, 'webrender_livekit_input')
web.par.url = 'http://localhost:3000/td-auto-viewer.html'
web.par.resolution = [1920, 1080]
web.par.enableaudio = True
web.par.active = True
web.nodeX = -200
web.nodeY = 200

# Create NDI Out TOP
ndi = root.create(ndioutTOP, 'ndiout_livekit')
ndi.par.active = True
ndi.par.ndiname = 'TD-LiveKit-Output'
ndi.nodeX = 200
ndi.nodeY = 200

# Connect them
ndi.inputConnectors[0].connect(web)

# Write success to file
with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_success.txt', 'w') as f:
    f.write("SUCCESS\n")
    f.write(f"Web Render: {web.path}\n")
    f.write(f"NDI Out: {ndi.path}\n")
    f.write(f"Connected: {ndi.inputConnectors[0].connections[0].owner.path if ndi.inputConnectors[0].connections else 'NOT CONNECTED'}\n")

print("SETUP COMPLETE - Check td_setup_success.txt")
