"""
Generate LiveKit Token for TouchDesigner WebRender
Uses the same SDK as server.js for consistency
"""

import sys
import os
import subprocess

# Check if we have the livekit-server-sdk package
try:
    import jwt
    import time
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "PyJWT", "--break-system-packages"],
                  check=True, capture_output=True)
    import jwt
    import time

# LiveKit credentials
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
INPUT_ROOM = "claymation-live"

def generate_touchdesigner_token():
    """Generate a token for TouchDesigner to receive video"""
    
    print("="*60)
    print("LIVEKIT TOKEN GENERATOR FOR TOUCHDESIGNER")
    print("="*60)
    
    # Create identity
    identity = f"touchdesigner-receiver"
    
    # Create token payload
    now = int(time.time())
    exp = now + (24 * 60 * 60)  # 24 hours from now
    
    payload = {
        "video": {
            "room": INPUT_ROOM,
            "roomJoin": True,
            "canPublish": False,  # TouchDesigner won't publish to this room
            "canSubscribe": True   # TouchDesigner subscribes to camera feed
        },
        "iss": LIVEKIT_API_KEY,
        "sub": identity,
        "iat": now,
        "nbf": now,
        "exp": exp
    }
    
    # Generate JWT token
    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    
    print(f"\nGenerated token for TouchDesigner")
    print(f"Identity: {identity}")
    print(f"Room: {INPUT_ROOM}")
    print(f"Valid for: 24 hours")
    print(f"\n" + "="*60)
    print("COPY THIS TOKEN INTO TOUCHDESIGNER:")
    print("="*60)
    print(f"\n{token}\n")
    print("="*60)
    
    print("\nHOW TO USE THIS TOKEN IN TOUCHDESIGNER:")
    print("\n1. Find your webRenderTOP operator")
    print("   (Press Alt+L to search for 'webrender')")
    
    print("\n2. Open Parameters panel (right-click > Parameters)")
    
    print("\n3. Set these parameters:")
    print(f"   - Room Name: {INPUT_ROOM}")
    print(f"   - Server URL: {LIVEKIT_URL}")
    print("   - Token: [paste the token above]")
    print("   - Active: ON (checked)")
    
    print("\n4. Save your TouchDesigner project")
    
    print("\n5. Test:")
    print("   - Make sure publisher.html has camera running")
    print("   - WebRender should show the camera feed")
    
    # Save to file
    token_file = os.path.join(os.path.dirname(__file__), "touchdesigner_token.txt")
    with open(token_file, 'w') as f:
        f.write(f"LiveKit Token for TouchDesigner WebRender\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Valid until: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp))}\n")
        f.write(f"\nConfiguration:\n")
        f.write(f"Room: {INPUT_ROOM}\n")
        f.write(f"Server: {LIVEKIT_URL}\n")
        f.write(f"Identity: {identity}\n")
        f.write(f"\nToken (copy this):\n")
        f.write(f"{token}\n")
    
    print(f"\nToken also saved to: touchdesigner_token.txt")
    print("="*60)
    
    return token

if __name__ == "__main__":
    token = generate_touchdesigner_token()
    print("\nToken generated successfully!")
    input("\nPress Enter to close...")
