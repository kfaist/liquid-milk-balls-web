"""
Fix OBS WHIP Configuration - Use Correct LiveKit WHIP Subdomain
Based on successful config from earlier today
"""

import jwt
import time
import json

# LiveKit credentials
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"
ROOM_NAME = "processed-output"

print("="*60)
print("FIXING OBS WHIP CONFIGURATION")
print("="*60)

# Generate fresh token (24 hour expiry)
current_time = int(time.time())
exp_time = current_time + (24 * 60 * 60)

payload = {
    "video": {
        "room": ROOM_NAME,
        "roomJoin": True,
        "canPublish": True,
        "canSubscribe": False
    },
    "iss": LIVEKIT_API_KEY,
    "exp": exp_time,
    "nbf": 0,
    "sub": f"obs-{ROOM_NAME}"
}

token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")

print(f"\n[OK] Fresh token generated")
print(f"[INFO] Expires: {time.ctime(exp_time)}")

# CORRECT WHIP URL FORMAT (from successful session earlier)
# Use WHIP subdomain, NOT main domain
whip_server = "https://claymation-transcription-l6e51sws.whip.livekit.cloud/w"

print(f"\n[CORRECT FORMAT]")
print(f"Server: {whip_server}")
print(f"Bearer Token: {token}")
print(f"(Token goes in bearer_token field, NOT in URL!)")

# Create CORRECT OBS configuration
obs_config = {
    "type": "whip_custom",
    "settings": {
        "server": whip_server,  # WHIP subdomain, no token in URL
        "bearer_token": token,  # Token goes HERE
        "use_auth": False,
        "bwtest": False,
        "service": "WHIP"
    }
}

# Save to OBS config file
config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json"
with open(config_path, 'w') as f:
    json.dump(obs_config, f)

print(f"\n[SUCCESS] OBS configuration FIXED!")
print(f"[FILE] {config_path}")
print("\n" + "="*60)
print("WHAT WAS WRONG:")
print("- Old: Used main domain with token in URL")
print("- Fixed: Uses WHIP subdomain with token in bearer_token field")
print("\n" + "="*60)
print("NEXT: Restart OBS and click 'Start Streaming'")
print("="*60)
