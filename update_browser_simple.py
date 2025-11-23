"""
Update OBS Browser Source to use simple test page
This tests if Browser Source works at all before trying LiveKit
"""

import json

print("=" * 70)
print("UPDATING OBS BROWSER SOURCE - SIMPLE TEST")
print("=" * 70)

scene_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\scenes\Untitled.json"

print("\n[1/3] Loading OBS configuration...")
with open(scene_path, 'r', encoding='utf-8') as f:
    obs_config = json.load(f)

# Find Browser Source
browser_source = None
for source in obs_config['sources']:
    if source.get('id') == 'browser_source':
        browser_source = source
        break

if not browser_source:
    print("ERROR: Browser source not found!")
    exit(1)

print(f"Found: {browser_source['name']}")
print(f"Current URL: {browser_source['settings'].get('url', 'NOT SET')}")

print("\n[2/3] Updating to simple test page...")
browser_source['settings']['url'] = 'http://localhost:3000/browser-source-test.html'

print(f"New URL: {browser_source['settings']['url']}")

print("\n[3/3] Saving...")
with open(scene_path, 'w', encoding='utf-8') as f:
    json.dump(obs_config, f, indent=4)

print("Configuration saved!")
print("\n" + "=" * 70)
print("BROWSER SOURCE UPDATED")
print("=" * 70)
print("""
Restart OBS to test with simple page.

If you see a purple gradient with a clock:
  ✓ Browser Source works!
  Then we'll update to LiveKit page

If it still crashes:
  ✗ OBS Browser Source has a deeper issue
  We'll need alternative approach
""")
