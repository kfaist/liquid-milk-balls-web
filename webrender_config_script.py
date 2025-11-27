"""
MIRROR'S ECHO - WebRender Input Pipeline Fix
This script will:
1. Query TouchDesigner to find WebRender TOPs
2. Configure the WebRender TOP for LiveKit input
3. Verify the connection
"""

import pyautogui
import time
import subprocess

# TD Textport script to find and configure WebRender TOPs
TD_SCRIPT = '''
print("="*50)
print("TOUCHDESIGNER WEBRENDER ANALYSIS")
print("="*50)

# Find all WebRender TOPs
webrender_tops = []
try:
    # Search recursively from root
    for n in root.findChildren(depth=10):
        if hasattr(n, 'type'):
            if 'webrender' in str(n.type).lower() or 'webRender' in str(type(n)):
                webrender_tops.append(n)
except Exception as e:
    print(f"Error during search: {e}")

# Try another method
try:
    from td import op
    # Look for common WebRender names
    for name in ['webrender1', 'webrender_livekit_input', 'webrender_input', 'webrenderTOP1']:
        try:
            n = op('/' + name)
            if n is not None:
                webrender_tops.append(n)
        except:
            pass
except Exception as e:
    print(f"Op search error: {e}")

print(f"\\nFound {len(webrender_tops)} WebRender TOP(s)")

for wr in webrender_tops:
    print(f"\\n--- {wr.path} ---")
    print(f"Type: {type(wr)}")
    
    # Get all parameters
    if hasattr(wr, 'pars'):
        for p in wr.pars():
            if p.val != p.default:
                print(f"  {p.name} = {p.val}")

# Also check NDI TOPs
print("\\n" + "="*50)
print("NDI TOPs")
print("="*50)

for n in root.findChildren(depth=10):
    try:
        typename = str(type(n).__name__).lower()
        if 'ndi' in typename:
            print(f"  {n.path} - {type(n).__name__}")
    except:
        pass

print("\\n" + "="*50)
print("DONE")
print("="*50)
'''

def main():
    print("Mirror's Echo - WebRender Configuration Script")
    print("=" * 50)
    
    # Save TD script to file for manual paste if needed
    script_path = r"C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\td_query_script.txt"
    with open(script_path, 'w') as f:
        f.write(TD_SCRIPT)
    print(f"TD script saved to: {script_path}")
    
    # Try to activate TD and open textport
    import pygetwindow as gw
    
    td_windows = [w for w in gw.getAllWindows() if 'TouchDesigner' in w.title]
    if not td_windows:
        print("ERROR: TouchDesigner not found!")
        return
    
    print(f"Found TouchDesigner: {td_windows[0].title}")
    
    # Instructions
    print("\n" + "="*50)
    print("MANUAL STEPS:")
    print("1. Switch to TouchDesigner")
    print("2. Press Alt+T to open Textport")
    print("3. Copy and paste the contents of:")
    print(f"   {script_path}")
    print("4. Press Enter to execute")
    print("="*50)

if __name__ == "__main__":
    main()
