import subprocess
import time

print("="*60)
print("STARTING OBS (Stream Config Disabled)")
print("="*60)

# Kill any existing OBS
print("\n[1/3] Killing existing OBS...")
subprocess.run(['taskkill', '/IM', 'obs64.exe', '/F'], capture_output=True)
time.sleep(2)

# Start OBS fresh
print("\n[2/3] Starting OBS...")
subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])

# Wait and verify
print("\n[3/3] Waiting for OBS to load...")
for i in range(15):
    time.sleep(1)
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'],
                           capture_output=True, text=True, check=False)
    if 'obs64.exe' in result.stdout:
        print(f"[OK] OBS running after {i+1} seconds")
        break

print("\n" + "="*60)
print("OBS STARTED SUCCESSFULLY!")
print("\nStream config is disabled so OBS won't crash.")
print("Now we need to configure streaming manually in OBS UI.")
print("="*60)
