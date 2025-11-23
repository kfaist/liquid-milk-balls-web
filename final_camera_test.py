"""
FINAL TEST - Complete camera pipeline through OBS
"""
import subprocess
import time

print("=" * 80)
print("FINAL CAMERA TEST - OBS BROWSER SOURCE METHOD")
print("=" * 80)

print("\nWaiting 5 seconds for OBS to fully load...")
time.sleep(5)

print("\nOpening publisher.html in browser...")
subprocess.run(['powershell', '-Command', 'Start-Process "http://localhost:3000/publisher.html"'])
time.sleep(2)

print("\n" + "=" * 80)
print("COMPLETE THIS TEST NOW:")
print("=" * 80)
print("\n1. IN BROWSER TAB (publisher.html):")
print("   - Click 'Start Publishing' button")
print("   - Click 'Allow' when asked for camera")
print("   - You should see your camera preview")
print("")
print("2. IN OBS STUDIO:")
print("   - Look at 'LiveKit Camera Input' source")
print("   - Should show 'Connected - Waiting for camera'")
print("   - Then YOUR CAMERA should appear!")
print("")
print("3. IF CAMERA APPEARS IN OBS:")
print("   - SUCCESS! Input pipeline working!")
print("   - Camera goes: Browser → LiveKit → OBS")
print("   - OBS sends: NDI → TouchDesigner")
print("   - TD processes and sends: OBS → LiveKit → Viewers")
print("")
print("4. TEST COMPLETE LOOP:")
print("   - Open: http://localhost:3000/return-viewer.html")
print("   - Should see processed video!")
print("")
print("=" * 80)
