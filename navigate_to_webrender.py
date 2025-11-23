import pyautogui
import time

print("Navigating to TouchDesigner webrender operator...")

# Click on TouchDesigner window area (left side where TD is visible)
pyautogui.click(200, 400)
time.sleep(0.5)

# Search for operator (Ctrl+F in TD)
pyautogui.hotkey('ctrl', 'f')
time.sleep(0.5)

# Type operator name
pyautogui.write('webrender_livekit_input', interval=0.05)
time.sleep(0.5)

# Press Enter to go to it
pyautogui.press('enter')
time.sleep(1)

# Take screenshot
import subprocess
subprocess.run(['powershell', 
    'Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; ' +
    '$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; ' +
    '$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); ' +
    '$graphics = [System.Drawing.Graphics]::FromImage($bitmap); ' +
    '$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); ' +
    '$bitmap.Save("C:\\Users\\krista-showputer\\Desktop\\liquid-milk-balls-web\\screenshot_webrender.png")'])

print("Screenshot saved! Check screenshot_webrender.png")
