import subprocess
import time
import pyautogui

print("Switching to Firefox...")

# Activate Firefox
subprocess.run(['powershell',
    'Add-Type -AssemblyName Microsoft.VisualBasic; ' +
    '[Microsoft.VisualBasic.Interaction]::AppActivate("Firefox")'],
    shell=True)

time.sleep(2)

print("Firefox activated - ready for manual camera start!")
print("\nNEXT: Click 'Start Camera' button on the publisher page")
