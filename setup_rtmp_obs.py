"""
Setup OBS with RTMP to LiveKit (more reliable than WHIP)
"""

import jwt
import time
import json

# LiveKit credentials
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"
LIVEKIT_URL = "rtmps://claymation-transcription-l6e51sws.livekit.cloud:443/live"
ROOM_NAME = "processed-output"

print("="*60)
print("SWITCHING OBS TO RTMP (More Reliable)")
print("="*60)

# Generate stream key (LiveKit room + token)
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
    "sub": f"obs-rtmp-{ROOM_NAME}"
}

token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")

# RTMP stream key format: room_name?access_token=TOKEN
stream_key = f"{ROOM_NAME}?access_token={token}"

print(f"\n[OK] Generated RTMP configuration")
print(f"[INFO] Expires: {time.ctime(exp_time)}")

# Create OBS service.json for RTMP
obs_config = {
    "type": "rtmp_custom",
    "settings": {
        "server": LIVEKIT_URL,
        "key": stream_key,
        "use_auth": False,
        "bwtest": False
    }
}

# Save configuration
config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json"
with open(config_path, 'w') as f:
    json.dump(obs_config, f)

print(f"\n[SUCCESS] OBS configured for RTMP streaming")
print(f"[FILE] {config_path}")
print(f"\n[RTMP Server] {LIVEKIT_URL}")
print(f"[Stream Key] {stream_key[:50]}...")
print("\n" + "="*60)
print("RTMP is more reliable than WHIP!")
print("Next: Restart OBS and start streaming")
print("="*60)
