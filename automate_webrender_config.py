"""
Automated WebRender TOP Configuration
This script will automatically configure the WebRender TOP in TouchDesigner
"""

import pyautogui
import pyperclip
import time
import subprocess

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

print("=" * 80)
print("AUTOMATED TOUCHDESIGNER WEBRENDER TOP CONFIGURATION")
print("=" * 80)
print()

# Step 1: Read the configuration script
print("Step 1: Loading configuration script...")
with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/configure_webrender_td.py', 'r') as f:
    config_script = f.read()
print("[OK] Configuration script loaded")
print()

# Step 2: Copy script to clipboard
print("Step 2: Copying script to clipboard...")
pyperclip.copy(config_script)
print("[OK] Script copied to clipboard")
print()

# Step 3: Focus TouchDesigner window
print("Step 3: Focusing TouchDesigner window...")
try:
    subprocess.run([
        "powershell", 
        "-Command",
        "$win = Get-Process -Name 'TouchDesigner' -ErrorAction SilentlyContinue | Select-Object -First 1; " +
        "if ($win) { " +
        "    Add-Type @\"" +
        "        using System;" +
        "        using System.Runtime.InteropServices;" +
        "        public class Win32 {" +
        "            [DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);" +
        "            [DllImport(\"user32.dll\")] public static extern bool SetForegroundWindow(IntPtr hWnd);" +
        "        }" +
        "    \"@;" +
        "    $h = $win.MainWindowHandle;" +
        "    [Win32]::ShowWindow($h, 9);" +
        "    [Win32]::SetForegroundWindow($h);" +
        "}"
    ], check=True, capture_output=True)
    time.sleep(2)
    print("[OK] TouchDesigner window focused")
except Exception as e:
    print(f"[WARNING] Could not focus TouchDesigner: {e}")
    print("  Please manually focus TouchDesigner window")
print()

# Step 4: Open textport
print("Step 4: Opening TouchDesigner textport (Alt+T)...")
time.sleep(1)
pyautogui.hotkey('alt', 't')
time.sleep(1)
print("[OK] Textport opened")
print()

# Step 5: Clear textport
print("Step 5: Clearing textport...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)
print("[OK] Textport cleared")
print()

# Step 6: Paste and execute script
print("Step 6: Pasting configuration script...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)
print("[OK] Script pasted")
print()

print("Step 7: Executing script...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'enter')
time.sleep(2)
print("[OK] Script executed")
print()

print("=" * 80)
print("CONFIGURATION COMPLETE!")
print("=" * 80)
print()
print("Please check the TouchDesigner textport for configuration results.")
print()
print("NEXT STEPS:")
print("1. Verify the WebRender TOP shows the correct URL")
print("2. Check for any yellow warning triangles")
print("3. Open http://localhost:3000/publisher.html in a browser")
print("4. Click 'Start Publishing' to test the camera feed")
print()
print("=" * 80)
