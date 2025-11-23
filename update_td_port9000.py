import pyperclip

# Update webrender to port 9000 DEBUG viewer
td_script = """webrender = op('/project1/webrender_livekit')
webrender.par.url = 'http://localhost:9000/touchdesigner-viewer-DEBUG.html'
webrender.par.w = 1920
webrender.par.h = 1080
webrender.par.enableaudio = True
webrender.par.active = True
print('UPDATED TO PORT 9000 DEBUG VIEWER!')
"""

pyperclip.copy(td_script)
print("EXECUTING IN TD NOW...")
