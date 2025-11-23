"""
Get LiveKit Ingress for OBS WHIP Streaming
"""

from livekit import api
import os

# LiveKit credentials
LIVEKIT_URL = "https://claymation-transcription-l6e51sws.livekit.cloud"
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"
ROOM_NAME = "processed-output"

print("="*70)
print("CHECKING LIVEKIT INGRESS FOR OBS")
print("="*70)

# Create ingress client
ingress_client = api.IngressServiceClient(
    LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
)

print("\n[INFO] Listing existing ingress objects...")
try:
    ingress_list = ingress_client.list_ingress(room_name=ROOM_NAME)
    
    if ingress_list:
        print(f"[OK] Found {len(ingress_list)} ingress object(s)")
        
        for ingress in ingress_list:
            print(f"\n[INGRESS] {ingress.name}")
            print(f"  Ingress ID: {ingress.ingress_id}")
            print(f"  Room: {ingress.room_name}")
            print(f"  URL: {ingress.url}")
            print(f"  Stream Key: {ingress.stream_key}")
            print(f"  State: {ingress.state}")
            
            # Save the ingress info
            if ingress.state.name == "ENDPOINT_COMPLETE":
                print(f"\n[USE THIS] OBS WHIP Configuration:")
                print(f"  Server: {ingress.url}")
                print(f"  Stream Key: {ingress.stream_key}")
                
                import json
                obs_config = {
                    "type": "whip_custom",
                    "settings": {
                        "server": ingress.url,
                        "bearer_token": ingress.stream_key,
                        "use_auth": False,
                        "bwtest": False,
                        "service": "WHIP"
                    }
                }
                
                config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\profiles\Untitled\service.json"
                with open(config_path, 'w') as f:
                    json.dump(obs_config, f)
                
                print(f"\n[SUCCESS] Updated OBS config: {config_path}")
    else:
        print("[INFO] No ingress objects found")
        print("[ACTION] Creating new WHIP ingress...")
        
        # Create new ingress
        ingress_info = api.CreateIngressRequest(
            input_type=api.IngressInput.WHIP_INPUT,
            name=f"obs-{ROOM_NAME}",
            room_name=ROOM_NAME,
            participant_identity=f"obs-whip-{ROOM_NAME}",
            participant_name="OBS Studio"
        )
        
        new_ingress = ingress_client.create_ingress(ingress_info)
        
        print(f"\n[CREATED] New ingress")
        print(f"  URL: {new_ingress.url}")
        print(f"  Stream Key: {new_ingress.stream_key}")

except Exception as e:
    print(f"[ERROR] {e}")
    print(f"[INFO] Error type: {type(e).__name__}")

print("\n" + "="*70)
