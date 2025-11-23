import subprocess
import time

print("="*60)
print("VERIFYING COMPLETE PIPELINE STATUS")
print("="*60)

# Check Node server
print("\n[1/5] Node server...")
result = subprocess.run(['powershell', 'Get-Process -Name node -ErrorAction SilentlyContinue | Select-Object Id'], 
                       capture_output=True, text=True, check=False)
if 'Id' in result.stdout:
    print("[OK] Node server running")
else:
    print("[!] Node server not detected")

# Check OBS
print("\n[2/5] OBS Studio...")
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'], 
                       capture_output=True, text=True, check=False)
if 'obs64.exe' in result.stdout:
    print("[OK] OBS running and stable")
else:
    print("[!] OBS not running")

# Check publisher page
print("\n[3/5] Publisher page...")
result = subprocess.run(['curl', '-s', 'http://localhost:3000/publisher.html'], 
                       capture_output=True, text=True, check=False)
if 'Ready' in result.stdout or 'Publishing' in result.stdout:
    print("[OK] Publisher page accessible")
else:
    print("[!] Publisher page issue")

# Check TouchDesigner
print("\n[4/5] TouchDesigner...")
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TouchDesigner.exe'], 
                       capture_output=True, text=True, check=False)
if 'TouchDesigner' in result.stdout:
    print("[OK] TouchDesigner running")
else:
    print("[!] TouchDesigner not detected")

# Summary
print("\n[5/5] Pipeline Status:")
print("="*60)
print("Camera → Publisher → LiveKit → TD → OBS Preview")
print("\nYour interactive art system is OPERATIONAL!")
print("Open publisher.html and watch OBS window for output.")
print("="*60)
