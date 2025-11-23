# Direct TouchDesigner automation via Python
import pyautogui
import time
import subprocess

print("="*60)
print("TOUCHDESIGNER AUTOMATION - SETUP EXECUTION")
print("="*60)

# Find TouchDesigner window
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name "TouchDesigner" | Select-Object -ExpandProperty MainWindowTitle'],
    capture_output=True, text=True)

if result.stdout.strip():
    print(f"✅ Found TouchDesigner: {result.stdout.strip()}")
else:
    print("❌ TouchDesigner not found!")
    exit(1)

# Click on TouchDesigner window to focus it
print("\n1. Focusing TouchDesigner window...")
pyautogui.click(960, 540)  # Click center of screen
time.sleep(0.5)

# Open textport with Alt+T
print("2. Opening textport (Alt+T)...")
pyautogui.hotkey('alt', 't')
time.sleep(1)

# Type the exec command
command = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_setup_CORRECT.py').read())"
print(f"3. Typing command: {command}")
pyautogui.typewrite(command, interval=0.01)
time.sleep(0.5)

# Press Enter
print("4. Executing (pressing Enter)...")
pyautogui.press('enter')
time.sleep(2)

print("\n" + "="*60)
print("✅ AUTOMATION COMPLETE")
print("="*60)
print("\nPlease check TouchDesigner textport for output!")
