# Update OBS NDI source configuration

import json

print("="*60)
print("UPDATING OBS NDI SOURCE CONFIGURATION")
print("="*60)

# Read the scene file
scene_file = r'C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\scenes\Untitled.json'

with open(scene_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Find and update the NDI source
updated = False
for source in config['sources']:
    if source['id'] == 'ndi_source':
        old_name = source['settings']['ndi_source_name']
        source['settings']['ndi_source_name'] = 'KRISTA-SHOWPUTER-01 (TD-LiveKit-Output)'
        print(f"\nUpdated NDI Source:")
        print(f"   From: {old_name}")
        print(f"   To: KRISTA-SHOWPUTER-01 (TD-LiveKit-Output)")
        updated = True
        break

if not updated:
    print("\nERROR: NDI source not found!")
else:
    # Save backup
    backup_file = scene_file + '.backup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print(f"\nSaved backup to: {backup_file}")

    # Save updated config
    with open(scene_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print(f"Saved updated config to: {scene_file}")

    print("\n" + "="*60)
    print("CONFIGURATION UPDATED!")
    print("="*60)
    print("\nNow restart OBS to apply the changes:")
    print("1. Close OBS")
    print("2. Reopen OBS")
    print("3. The NDI source should now show TouchDesigner video!")
