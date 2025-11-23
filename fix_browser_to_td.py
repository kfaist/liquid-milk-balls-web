"""
FIX BROWSER TO TOUCHDESIGNER - Complete diagnostic and fix
"""
import subprocess
import time

print("=" * 80)
print("FIXING BROWSER TO TOUCHDESIGNER CONNECTION")
print("=" * 80)

# Test 1: Check td-auto-viewer.html directly in browser
print("\nStep 1: Testing td-auto-viewer.html in browser...")
print("Opening both pages in browser...")

# Open viewer page
subprocess.run(['powershell', '-Command', 'Start-Process "http://localhost:3000/td-auto-viewer.html"'])
time.sleep(2)

# Open publisher page
subprocess.run(['powershell', '-Command', 'Start-Process "http://localhost:3000/publisher.html"'])
time.sleep(2)

print("\n" + "=" * 80)
print("MANUAL TEST - DO THIS NOW:")
print("=" * 80)
print("\n🔴 IN PUBLISHER.HTML TAB:")
print("1. Click 'Start Publishing'")
print("2. Allow camera")
print("3. You should see your camera")
print("")
print("🔵 IN TD-AUTO-VIEWER.HTML TAB:")
print("1. You should see camera appear!")
print("2. Same camera from publisher")
print("")
print("=" * 80)
print("\nIf td-auto-viewer.html shows camera in BROWSER:")
print("  ✓ LiveKit connection working!")
print("  → Problem is webrender1 loading the page")
print("")
print("If td-auto-viewer.html does NOT show camera:")
print("  ✗ LiveKit connection broken")
print("  → Need to fix server/LiveKit first")
print("")
print("=" * 80)

input("\nDid you see camera in td-auto-viewer.html browser tab? (Press Enter when checked)")

print("\nStep 2: Now configuring webrender1 with EXACT same URL...")
print("This proves: If browser can show it, TouchDesigner can show it")
