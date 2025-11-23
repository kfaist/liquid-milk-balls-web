"""
Restart OBS to apply new browser source URL
"""
import subprocess
import time

print("=" * 80)
print("RESTARTING OBS")
print("=" * 80)

# Kill OBS
print("\nStep 1: Closing OBS...")
subprocess.run(['powershell', '-Command', 'Stop-Process -Name obs64 -Force'], 
               capture_output=True)
time.sleep(3)

# Start OBS
print("\nStep 2: Starting OBS...")
obs_path = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
subprocess.Popen([obs_path])
time.sleep(5)

print("\n" + "=" * 80)
print("OBS RESTARTED!")
print("=" * 80)
print("\nBrowser source now points to: td-auto-viewer.html")
print("\nNEXT STEPS:")
print("1. Check OBS - LiveKit Camera Input source should show viewer page")
print("2. Open publisher.html in browser")
print("3. Click 'Start Publishing'")
print("4. Camera appears in OBS!")
print("")
print("=" * 80)
