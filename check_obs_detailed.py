"""
Detailed OBS Status Check
"""

import sys

try:
    from obsws_python import ReqClient
except ImportError:
    print("Installing obsws-python...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "obsws-python", "--break-system-packages"], check=True)
    from obsws_python import ReqClient

def main():
    print("="*70)
    print("DETAILED OBS STATUS CHECK")
    print("="*70)
    
    try:
        client = ReqClient(host="localhost", port=4455, password="", timeout=5)
        print("\n✓ Connected to OBS WebSocket")
        
        # Get streaming status
        print("\n[STREAMING STATUS]")
        stream_status = client.get_stream_status()
        print(f"  Active: {stream_status.output_active}")
        if stream_status.output_active:
            print(f"  Duration: {stream_status.output_duration / 1000:.1f}s")
            print(f"  Bytes sent: {stream_status.output_bytes}")
            print(f"  Reconnecting: {stream_status.output_reconnecting}")
        
        # Get scenes
        print("\n[SCENES]")
        scenes = client.get_scene_list()
        print(f"  Current Scene: {scenes.current_program_scene_name}")
        print(f"  Available Scenes: {[s['sceneName'] for s in scenes.scenes]}")
        
        # Get sources in current scene
        print("\n[SOURCES IN CURRENT SCENE]")
        scene_items = client.get_scene_item_list(scenes.current_program_scene_name)
        for item in scene_items.scene_items:
            print(f"  - {item['sourceName']} (ID: {item['sceneItemId']})")
            
        # Try to get recording status
        print("\n[RECORDING STATUS]")
        try:
            rec_status = client.get_record_status()
            print(f"  Active: {rec_status.output_active}")
        except:
            print("  Not recording")
            
        # Get stream service settings
        print("\n[STREAM SERVICE]")
        try:
            service_settings = client.get_stream_service_settings()
            print(f"  Type: {service_settings.stream_service_type}")
            print(f"  Settings: {service_settings.stream_service_settings}")
        except Exception as e:
            print(f"  Error getting service settings: {e}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
