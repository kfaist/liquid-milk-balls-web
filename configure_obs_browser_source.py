"""
Complete OBS configuration with Browser Source for remote camera input
Autonomous execution - no user intervention needed
"""

import json
import time

print("=" * 70)
print("CONFIGURING OBS FOR REMOTE CAMERA INPUT")
print("=" * 70)

# Load current OBS scene configuration
scene_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\scenes\Untitled.json"

print("\n[1/5] Loading OBS scene configuration...")
with open(scene_path, 'r', encoding='utf-8') as f:
    obs_config = json.load(f)

print("Current scene loaded successfully")
print(f"Current sources: {len(obs_config['sources'])}")

# Check if Browser Source already exists
existing_browser = None
for source in obs_config['sources']:
    if source.get('id') == 'browser_source':
        existing_browser = source
        break

if existing_browser:
    print("\n[2/5] Browser source already exists, updating configuration...")
    browser_source = existing_browser
else:
    print("\n[2/5] Creating new Browser Source for LiveKit camera input...")
    import uuid
    browser_source = {
        "prev_ver": 520093698,
        "name": "LiveKit Camera Input",
        "uuid": str(uuid.uuid4()),
        "id": "browser_source",
        "versioned_id": "browser_source",
        "settings": {},
        "mixers": 0,
        "sync": 0,
        "flags": 0,
        "volume": 1.0,
        "balance": 0.5,
        "enabled": True,
        "muted": False,
        "push-to-mute": False,
        "push-to-mute-delay": 0,
        "push-to-talk": False,
        "push-to-talk-delay": 0,
        "hotkeys": {},
        "deinterlace_mode": 0,
        "deinterlace_field_order": 0,
        "monitoring_type": 0,
        "private_settings": {}
    }
    obs_config['sources'].append(browser_source)

# Configure Browser Source settings
print("\n[3/5] Configuring Browser Source...")
browser_source['settings'] = {
    "url": "http://localhost:3000/td-auto-viewer.html",
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "shutdown": False,  # Don't shutdown when not visible
    "restart_when_active": True,  # Refresh when scene becomes active
    "css": "",
    "reroute_audio": True,
    "webpage_control_level": 1
}

print("Browser Source configured:")
print(f"  URL: http://localhost:3000/td-auto-viewer.html")
print(f"  Resolution: 1920x1080")
print(f"  FPS: 30")
print(f"  Auto-refresh: ON")

# Add Browser Source to the Scene's items list
print("\n[4/5] Adding Browser Source to Scene...")
scene = None
for source in obs_config['sources']:
    if source.get('name') == 'Scene':
        scene = source
        break

if scene and 'settings' in scene and 'items' in scene['settings']:
    # Check if already in scene
    browser_in_scene = False
    for item in scene['settings']['items']:
        if item.get('source_uuid') == browser_source['uuid']:
            browser_in_scene = True
            break
    
    if not browser_in_scene:
        # Get next ID
        next_id = scene['settings'].get('id_counter', 7) + 1
        scene['settings']['id_counter'] = next_id
        
        # Add to scene
        scene['settings']['items'].append({
            "name": "LiveKit Camera Input",
            "source_uuid": browser_source['uuid'],
            "visible": True,
            "locked": False,
            "rot": 0.0,
            "scale_ref": {"x": 1920.0, "y": 1080.0},
            "align": 5,
            "bounds_type": 0,
            "bounds_align": 0,
            "bounds_crop": False,
            "crop_left": 0,
            "crop_top": 0,
            "crop_right": 0,
            "crop_bottom": 0,
            "id": next_id,
            "group_item_backup": False,
            "pos": {"x": 0.0, "y": 0.0},
            "pos_rel": {"x": 0.0, "y": 0.0},
            "scale": {"x": 1.0, "y": 1.0},
            "scale_rel": {"x": 1.0, "y": 1.0},
            "bounds": {"x": 0.0, "y": 0.0},
            "bounds_rel": {"x": 0.0, "y": 0.0},
            "scale_filter": "disable",
            "blend_method": "default",
            "blend_type": "normal",
            "show_transition": {"duration": 0},
            "hide_transition": {"duration": 0},
            "private_settings": {}
        })
        print("Browser Source added to Scene")
    else:
        print("Browser Source already in Scene")

# Save backup
print("\n[5/5] Saving configuration...")
backup_path = scene_path + f".backup_{int(time.time())}"
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(obs_config, f, indent=4)
print(f"Backup saved: {backup_path}")

# Save new configuration
with open(scene_path, 'w', encoding='utf-8') as f:
    json.dump(obs_config, f, indent=4)
print(f"Configuration saved: {scene_path}")

print("\n" + "=" * 70)
print("OBS CONFIGURATION COMPLETE!")
print("=" * 70)
print("""
NEXT STEPS:
1. Restart OBS to load new configuration
2. You should see "LiveKit Camera Input" in your sources
3. Open publisher.html in browser and click 'Start Publishing'
4. The Browser Source will show the remote camera!

OBS will need to be restarted for changes to take effect.
""")
