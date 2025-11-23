"""
OBS WebSocket Configuration Enabler
Manually edits the global.ini to enable WebSocket
"""

def enable_websocket():
    """Add WebSocket configuration to OBS global.ini"""
    config_path = r"C:\Users\krista-showputer\AppData\Roaming\obs-studio\global.ini"
    
    try:
        # Read the file with UTF-8-SIG to handle BOM
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        # Check if WebSocket section already exists
        has_websocket = any('[OBSWebSocket]' in line for line in lines)
        
        if not has_websocket:
            # Add WebSocket section at the end
            websocket_config = [
                '\n',
                '[OBSWebSocket]\n',
                'ServerEnabled=true\n',
                'ServerPort=4455\n',
                'AlertsEnabled=true\n',
                'AuthRequired=false\n',
                'ServerPassword=\n'
            ]
            
            lines.extend(websocket_config)
            
            # Write back
            with open(config_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(lines)
            
            print("[OK] WebSocket configuration added to global.ini")
            print("[INFO] Settings:")
            print("  - Server Enabled: true")
            print("  - Server Port: 4455")
            print("  - Auth Required: false")
            return True
        else:
            print("[INFO] WebSocket section already exists in config")
            # Update the values
            in_websocket = False
            for i, line in enumerate(lines):
                if '[OBSWebSocket]' in line:
                    in_websocket = True
                elif line.startswith('['):
                    in_websocket = False
                elif in_websocket:
                    if line.startswith('ServerEnabled'):
                        lines[i] = 'ServerEnabled=true\n'
                    elif line.startswith('AuthRequired'):
                        lines[i] = 'AuthRequired=false\n'
            
            with open(config_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(lines)
            print("[OK] WebSocket configuration updated")
            return True
            
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def main():
    print("="*60)
    print("ENABLING OBS WEBSOCKET")
    print("="*60)
    
    if enable_websocket():
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print("\nNext steps:")
        print("1. Close OBS if it's running")
        print("2. Start OBS")
        print("3. WebSocket should now be enabled automatically")
        print("4. Run: python obs_start_stream.py")
    else:
        print("\n[FAIL] Could not enable WebSocket")
        print("Please enable manually in OBS:")
        print("  Tools > WebSocket Server Settings")

if __name__ == "__main__":
    main()
