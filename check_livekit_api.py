"""
Check LiveKit Server API for correct ingress method
"""

try:
    import livekit
    print("LiveKit package contents:")
    print(dir(livekit))
    print("\n")
    
    if hasattr(livekit, 'api'):
        print("livekit.api contents:")
        print(dir(livekit.api))
        print("\n")
        
    # Try to create access token for WHIP
    from livekit import api
    import time
    
    token = api.AccessToken("APITw2Yp2Tv3yfg", "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW")
    token.with_identity("obs-processed-output")
    token.with_name("OBS Studio")
    token.with_grants(api.VideoGrants(
        room_join=True,
        room="processed-output",
        can_publish=True,
        can_subscribe=False
    ))
    
    jwt_token = token.to_jwt()
    print(f"Generated WHIP token: {jwt_token}")
    print(f"\nWHIP URL: https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token={jwt_token}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
