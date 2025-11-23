"""
Test the complete INPUT path for video processing pipeline
"""

import requests
import json

print("=" * 60)
print("TESTING VIDEO INPUT PATH")
print("=" * 60)

# Test 1: Server is running
print("\n[1/4] Checking server...")
try:
    response = requests.get("http://localhost:3000", timeout=5)
    if response.status_code == 200:
        print("[OK] Server running on port 3000")
    else:
        print(f"[FAIL] Server returned {response.status_code}")
except Exception as e:
    print(f"[FAIL] Server not accessible: {e}")
    exit(1)

# Test 2: Publisher page loads
print("\n[2/4] Checking publisher page...")
try:
    response = requests.get("http://localhost:3000/publisher.html", timeout=5)
    if response.status_code == 200:
        print("[OK] publisher.html loads successfully")
        if "livekit" in response.text.lower():
            print("[OK] Publisher contains LiveKit code")
    else:
        print(f"[FAIL] Publisher returned {response.status_code}")
except Exception as e:
    print(f"[FAIL] Publisher page error: {e}")

# Test 3: td-auto-viewer loads  
print("\n[3/4] Checking td-auto-viewer page...")
try:
    response = requests.get("http://localhost:3000/td-auto-viewer.html", timeout=5)
    if response.status_code == 200:
        print("[OK] td-auto-viewer.html loads successfully")
        if "viewer-token" in response.text.lower():
            print("[OK] Viewer configured for /api/viewer-token")
    else:
        print(f"[FAIL] Viewer returned {response.status_code}")
except Exception as e:
    print(f"[FAIL] Viewer page error: {e}")

# Test 4: Token API works
print("\n[4/4] Checking viewer token API...")
try:
    response = requests.get("http://localhost:3000/api/viewer-token", timeout=5)
    if response.status_code == 200:
        data = response.json()
        if data.get('token') and data.get('serverUrl'):
            print("[OK] Viewer token API working")
            print(f"  Room: {data.get('roomName', 'unknown')}")
            print(f"  Server: {data.get('serverUrl', 'unknown')[:50]}...")
        else:
            print("[FAIL] Token API returned invalid data")
    else:
        print(f"[FAIL] Token API returned {response.status_code}")
except Exception as e:
    print(f"[FAIL] Token API error: {e}")

# Summary
print("\n" + "=" * 60)
print("INPUT PATH SUMMARY")
print("=" * 60)
print("""
For video to flow INTO TouchDesigner:

STEP 1: Open publisher.html in browser
  URL: http://localhost:3000/publisher.html
  
STEP 2: Click 'Start Publishing' to send camera to LiveKit

STEP 3: In TouchDesigner, create WebRender TOP operator
  - Add a Web Render TOP to your network
  - Set URL parameter to: http://localhost:3000/td-auto-viewer.html
  - Enable Active checkbox
  
STEP 4: Connect WebRender output to your effects
  - The WebRender TOP will display the LiveKit camera stream
  - Connect it to your processing operators
  
Then your OUTPUT flows:
Processing -> NDI Out -> OBS -> WHIP -> LiveKit -> return-viewer.html
""")
