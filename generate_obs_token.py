"""
Generate fresh LiveKit WHIP token for OBS streaming
"""

import jwt
import time
import json

# LiveKit credentials from .env
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
ROOM_NAME = "processed-output"

print("="*60)
print("GENERATING FRESH LIVEKIT WHIP TOKEN FOR OBS")
print("="*60)

# Generate token (valid for 24 hours)
current_time = int(time.time())
exp_time = current_time + (24 * 60 * 60)  # 24 hours from now

# Token payload
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

# Generate token
token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")

print(f"\n[OK] Token generated successfully!")
print(f"[INFO] Valid for 24 hours (expires: {time.ctime(exp_time)})")
print(f"\n[TOKEN] {token}")

# Construct WHIP URL
whip_url = f"https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token={token}"

print(f"\n[WHIP URL]")
print(whip_url)

# Create OBS service.json configuration
obs_config = {
    "type": "whip_custom",
    "settings": {
        "server": whip_url,
        "use_auth": False,
        "bwtest": False,
        "service": "WHIP",
        "bearer_token": ""
    }
}

# Save to file
config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json"
with open(config_path, 'w') as f:
    json.dump(obs_config, f)

print(f"\n[SUCCESS] Updated OBS configuration!")
print(f"[FILE] {config_path}")
print("\n" + "="*60)
print("NEXT STEPS:")
print("1. Restart OBS Studio (close and reopen)")
print("2. Click 'Start Streaming' button")
print("3. Should connect successfully now!")
print("="*60)
