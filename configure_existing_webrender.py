import pyperclip

# Script to configure the existing webrender_livekit operator
td_script = """# Configure webrender_livekit for LiveKit stream
webrender = op('/project1/webrender_livekit')
webrender.par.url = 'http://localhost:3000/td-auto-viewer.html'
webrender.par.w = 1920
webrender.par.h = 1080
webrender.par.enableaudio = True
webrender.par.active = True
print('LiveKit Web Render configured!')
print('URL: http://localhost:3000/td-auto-viewer.html')
print('Active: ON')
"""

pyperclip.copy(td_script)
print("CONFIGURATION SCRIPT COPIED!")
print()
print("This will configure /project1/webrender_livekit")
print()
print("STEPS:")
print("1. In TD, press ALT+T for textport")
print("2. Paste with CTRL+V")
print("3. Press ENTER")
print()
print("Then open http://localhost:3000/publisher.html in a browser")
print("and click 'Start Publishing' to see video in TD!")
