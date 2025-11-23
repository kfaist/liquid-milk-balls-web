"""
Fix OBS Browser Source - Change URL to td-auto-viewer.html
"""
import json
import shutil
from datetime import datetime

obs_config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\scenes\Untitled.json"
backup_path = f"{obs_config_path}.backup_{int(datetime.now().timestamp())}"

print("=" * 80)
print("FIXING OBS BROWSER SOURCE URL")
print("=" * 80)

# Backup first
print(f"\nCreating backup: {backup_path}")
shutil.copy(obs_config_path, backup_path)

# Read config
with open(obs_config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Find and update Browser Source
print("\nSearching for LiveKit Camera Input source...")
updated = False

for source in config.get('sources', []):
    if source.get('name') == 'LiveKit Camera Input':
        print(f"Found source: {source['name']}")
        
        # Update URL in settings
        settings = source.get('settings', {})
        old_url = settings.get('url', '')
        new_url = 'http://localhost:3000/td-auto-viewer.html'
        
        print(f"  Old URL: {old_url}")
        print(f"  New URL: {new_url}")
        
        settings['url'] = new_url
        source['settings'] = settings
        updated = True
        break

if updated:
    # Save config
    with open(obs_config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print("\n✓ OBS config updated successfully!")
    print("\nNEXT STEPS:")
    print("1. Restart OBS (close and reopen)")
    print("2. Browser source will now show td-auto-viewer.html")
    print("3. Open publisher.html in browser")
    print("4. Click 'Start Publishing'")
    print("5. Camera should appear in OBS!")
else:
    print("\n✗ Could not find 'LiveKit Camera Input' source")
    print("Manual fix needed")

print("\n" + "=" * 80)
