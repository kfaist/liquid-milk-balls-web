# Add LiveKit Web Render TOP to TouchDesigner
import pyperclip

td_script = """# Create Web Render TOP for LiveKit input
webrender = op('/').create(webRenderTOP, 'livekit_input')
webrender.par.url = 'http://localhost:3000/td-auto-viewer.html'
webrender.par.w = 1920
webrender.par.h = 1080
webrender.par.enableaudio = True
webrender.par.active = True
webrender.nodeX = 0
webrender.nodeY = 0
print('LiveKit Web Render TOP created at /livekit_input')
"""

pyperclip.copy(td_script)
print("SCRIPT COPIED TO CLIPBOARD!")
print()
print("NEXT STEPS:")
print("1. Click on TouchDesigner window")
print("2. Press ALT+T to open textport")  
print("3. Paste with CTRL+V")
print("4. Press ENTER")
print()
print("This will create: /livekit_input")
print("URL: http://localhost:3000/td-auto-viewer.html")
