import subprocess
import time
import pyautogui

print("="*60)
print("STARTING OBS AND ACTIVATING STREAMING")
print("="*60)

# Start OBS
print("\n[1/5] Starting OBS...")
subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])
print("[OK] OBS launch command sent")

# Wait for OBS to load
print("\n[2/5] Waiting for OBS to load (20 seconds)...")
for i in range(20):
    time.sleep(1)
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq obs64.exe'], 
                           capture_output=True, text=True, check=False)
    if 'obs64.exe' in result.stdout:
        print(f"[OK] OBS running after {i+1} seconds")
        break

# Extra wait for UI
print("[INFO] Waiting for UI to fully load...")
time.sleep(5)

# Activate window - multiple attempts
print("\n[3/5] Activating OBS window...")
for attempt in range(3):
    try:
        # Click center screen to activate
        screen_w, screen_h = pyautogui.size()
        pyautogui.click(screen_w // 2, screen_h // 2)
        time.sleep(1)
        print(f"[INFO] Activation attempt {attempt + 1}")
    except:
        pass

# Locate and click Start Streaming
print("\n[4/5] Finding Start Streaming button...")
screen_w, screen_h = pyautogui.size()
print(f"[INFO] Screen: {screen_w}x{screen_h}")

# Calculate button position
button_x = int(screen_w * 0.87)
button_y = int(screen_h * 0.75)
print(f"[INFO] Button estimated at: ({button_x}, {button_y})")

# Move and click
print("\n[5/5] Clicking Start Streaming...")
pyautogui.moveTo(button_x, button_y, duration=0.5)
time.sleep(0.5)
pyautogui.click()
time.sleep(3)

print("\n" + "="*60)
print("DONE! OBS SHOULD BE STREAMING NOW!")
print("\nVerify:")
print("1. OBS shows 'Stop Streaming' button")
print("2. Status bar shows bitrate")
print("3. return-viewer.html shows video")
print("="*60)
