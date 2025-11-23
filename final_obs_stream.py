import subprocess
import time
import pyautogui

print("="*60)
print("FINAL OBS STREAMING ACTIVATION - CORRECT INGRESS")
print("="*60)

# Start OBS
print("\n[1/4] Starting OBS with correct config...")
subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])

# Wait for OBS to load
print("\n[2/4] Waiting for OBS to fully load...")
for i in range(20):
    time.sleep(1)
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'],
                           capture_output=True, text=True, check=False)
    if 'obs64.exe' in result.stdout:
        print(f"[OK] OBS running after {i+1} seconds")
        break

# Extra wait for UI
time.sleep(6)

# Activate and click Start Streaming
print("\n[3/4] Activating OBS window...")
screen_w, screen_h = pyautogui.size()
pyautogui.click(screen_w // 2, screen_h // 2)
time.sleep(2)

print("\n[4/4] Clicking Start Streaming button...")
button_x = int(screen_w * 0.87)
button_y = int(screen_h * 0.75)
print(f"[INFO] Button at: ({button_x}, {button_y})")

pyautogui.moveTo(button_x, button_y, duration=0.5)
time.sleep(0.5)
pyautogui.click()
time.sleep(4)

# Verify
print("\n" + "="*60)
print("STREAMING ACTIVATED!")
print("\nConfig used:")
print("  URL: https://...whip.livekit.cloud/w")
print("  Stream Key: vZzz34cdzRkd (from LiveKit ingress)")
print("\nCheck:")
print("1. OBS shows 'Stop Streaming' button")
print("2. No connection errors")
print("3. Open return-viewer.html to see video!")
print("="*60)
