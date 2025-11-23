import pyperclip

# Check TD webrender status
td_script = """webrender = op('/project1/webrender_livekit')
print('=' * 60)
print('WEB RENDER TOP STATUS:')
print('=' * 60)
print('URL:', webrender.par.url)
print('Active:', webrender.par.active)
print('Resolution:', webrender.par.w, 'x', webrender.par.h)
print('Enable Audio:', webrender.par.enableaudio)
print('=' * 60)
# Force reload the page
webrender.par.reload.pulse()
print('RELOADED WEB RENDER TOP!')
"""

pyperclip.copy(td_script)
print("Script copied to clipboard!")
print()
print("In TouchDesigner:")
print("1. Press ALT+T for textport")
print("2. Paste (CTRL+V)")
print("3. Press ENTER")
print()
print("This will show status and reload the web render")
