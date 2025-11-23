"""
Check OBS scenes configuration to see all sources
"""
import json

obs_config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\basic\scenes\Untitled.json"

print("=" * 80)
print("OBS SOURCES CONFIGURATION")
print("=" * 80)

with open(obs_config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# List all sources
print("\nSOURCES IN OBS:")
print("-" * 80)
for i, source in enumerate(config.get('sources', []), 1):
    name = source.get('name', 'Unknown')
    source_type = source.get('id', 'Unknown')
    enabled = source.get('enabled', True)
    settings = source.get('settings', {})
    
    print(f"\n{i}. {name}")
    print(f"   Type: {source_type}")
    print(f"   Enabled: {enabled}")
    
    if source_type == 'browser_source':
        url = settings.get('url', 'No URL')
        width = settings.get('width', 0)
        height = settings.get('height', 0)
        print(f"   URL: {url}")
        print(f"   Size: {width}x{height}")
    elif source_type == 'ndi_source':
        source_name = settings.get('ndi_source_name', 'Not set')
        print(f"   NDI Source: {source_name}")

print("\n" + "=" * 80)
