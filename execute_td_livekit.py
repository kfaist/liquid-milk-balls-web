import pyautogui
import time
import subprocess

print("Focusing TouchDesigner and executing script...")

# Find and focus TouchDesigner window
subprocess.run(['powershell', '-Command', """
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('TouchDesigner')
Start-Sleep -Milliseconds 500
"""], check=False)

time.sleep(1)

# Open textport with ALT+T
pyautogui.hotkey('alt', 't')
time.sleep(0.5)

# Paste the script (already in clipboard)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.3)

# Execute with ENTER
pyautogui.press('enter')

print("Script executed in TouchDesigner!")
print("Check TD for /livekit_input operator")
