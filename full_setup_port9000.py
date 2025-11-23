import pyperclip
import pyautogui
import time
import subprocess

print("CONFIGURING TD FOR PORT 9000 DEBUG VIEWER")

td_script = """webrender = op('/project1/webrender_livekit')
webrender.par.url = 'http://localhost:9000/touchdesigner-viewer-DEBUG.html'
webrender.par.w = 1920
webrender.par.h = 1080
webrender.par.enableaudio = True
webrender.par.active = True
print('UPDATED TO PORT 9000 DEBUG VIEWER!')
print('URL: http://localhost:9000/touchdesigner-viewer-DEBUG.html')
"""

pyperclip.copy(td_script)

subprocess.run(['powershell', '-Command', """
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('TouchDesigner')
Start-Sleep -Milliseconds 500
"""], check=False)
time.sleep(1)

pyautogui.hotkey('alt', 't')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.3)
pyautogui.press('enter')

print("TD configured!")
print("Opening publisher...")

subprocess.Popen(['firefox', 'http://localhost:3000/publisher.html'])
time.sleep(2)

print("DONE!")
print("NEXT: Click Start Publishing in Firefox")
