"""
Open publisher and create instructions for camera test
"""
import subprocess
import time

print("=" * 80)
print("WEBRENDER1 IS CONNECTED - NOW TESTING CAMERA INPUT")
print("=" * 80)

print("\nGOOD NEWS:")
print("- webrender1 is active and working!")
print("- Shows '[TD-VIEWER] Connected' - LiveKit connection successful!")
print("- URL is correctly set to td-auto-viewer.html")
print("")

print("NEXT: Send camera from browser to make it appear in webrender1")
print("")

# Open publisher page
print("Opening publisher.html in browser...")
subprocess.run(['powershell', '-Command', 'Start-Process "http://localhost:3000/publisher.html"'])
time.sleep(2)

print("\n" + "=" * 80)
print("DO THIS NOW IN BROWSER:")
print("=" * 80)
print("")
print("1. Browser tab should open with publisher.html")
print("2. You'll see:")
print("   - Black background")
print("   - 'PUBLISHER' title")
print("   - 'Start Publishing' button")
print("")
print("3. CLICK 'Start Publishing'")
print("")
print("4. Browser asks: 'Allow camera?'")
print("   - CLICK 'Allow'")
print("")
print("5. WATCH TOUCHDESIGNER webrender1:")
print("   - Should show YOUR CAMERA!")
print("   - Text changes to show video feed")
print("")
print("=" * 80)
print("")
print("If camera appears in webrender1:")
print("  SUCCESS! Input pipeline complete!")
print("  You can then connect it to your effects!")
print("")
print("=" * 80)
