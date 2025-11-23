"""
Check if publisher.html is working and camera is streaming
Open the page and check console
"""
import webbrowser
import time

print("=" * 80)
print("TESTING CAMERA PUBLISHER")
print("=" * 80)

print("\nOpening publisher.html in browser...")
webbrowser.open('http://localhost:3000/publisher.html')

time.sleep(3)

print("\n" + "=" * 80)
print("MANUAL CHECKS NEEDED:")
print("=" * 80)
print("\nIn the browser window that just opened:")
print("")
print("1. Do you see the 'Start Publishing' button?")
print("   → If NO: Server issue")
print("   → If YES: Continue to step 2")
print("")
print("2. Click 'Start Publishing'")
print("   → Browser should ask for camera permission")
print("")
print("3. Click 'Allow' for camera access")
print("   → You should see your camera preview")
print("   → Status should change to 'Publishing'")
print("")
print("4. Open browser console (Press F12)")
print("   → Look for '[PUBLISHER] Connected to room' message")
print("   → Look for '[PUBLISHER] Publishing camera track' message")
print("")
print("=" * 80)
print("\nIf camera IS publishing:")
print("  → Problem is in TouchDesigner webrender")
print("  → Try alternative: Use local camera in TD instead")
print("")
print("If camera NOT publishing:")
print("  → Check browser console for errors")
print("  → LiveKit connection issue")
print("=" * 80)
