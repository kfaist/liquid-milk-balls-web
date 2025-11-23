import pyperclip

# Quick check of webrender URL
td_script = """webrender = op('/project1/webrender_livekit')
print('Current URL:', webrender.par.url)
print('Active:', webrender.par.active)
print('Resolution:', webrender.par.w, 'x', webrender.par.h)
"""

pyperclip.copy(td_script)
print("Script copied - paste in TD textport (ALT+T) to check URL")
