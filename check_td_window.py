import subprocess
import time

# Focus TD and take screenshot
print("Bringing TouchDesigner to front...")

subprocess.run(['powershell', '-Command', """
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('TouchDesigner')
Start-Sleep -Seconds 2
"""], check=False)

time.sleep(2)

# Take screenshot
import os
from PIL import ImageGrab
img = ImageGrab.grab()
save_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'liquid-milk-balls-web', 'td_focused.png')
img.save(save_path)
print(f"Screenshot saved: {save_path}")
