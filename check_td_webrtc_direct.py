import pyautogui
import time
import pyperclip

def check_td_webrtc():
    """Check WebRTC and LiveKit configuration in TouchDesigner via textport"""
    
    print("Opening TouchDesigner textport and checking WebRTC/LiveKit configuration...")
    
    # Focus TouchDesigner window
    td_windows = pyautogui.getWindowsWithTitle("TouchDesigner")
    if td_windows:
        td_windows[0].activate()
        time.sleep(1)
        print("TouchDesigner window activated")
    else:
        print("TouchDesigner window not found!")
        return
    
    # Open textport (Alt+T)
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Clear textport first
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.5)
    
    # Create Python code to check WebRTC and LiveKit nodes
    check_code = '''
# Check for WebRTC and LiveKit nodes
print("="*50)
print("WEBRTC AND LIVEKIT NODE DIAGNOSIS")
print("="*50)

# Find all operators
webrtc_ops = []
livekit_ops = []
webrender_ops = []
ndi_ops = []

for op in root.findChildren(depth=100):
    name_lower = op.name.lower()
    
    if 'webrtc' in name_lower or 'rtc' in name_lower:
        webrtc_ops.append(op)
    if 'livekit' in name_lower or 'live' in name_lower:
        livekit_ops.append(op)
    if 'webrender' in name_lower or op.type == 'webrendertop':
        webrender_ops.append(op)
    if 'ndi' in name_lower or op.type in ['ndiintop', 'ndiouttop']:
        ndi_ops.append(op)

print("\\nWEBRTC NODES:")
if webrtc_ops:
    for op in webrtc_ops:
        print(f"  {op.path} ({op.type})")
        if hasattr(op.par, 'active'):
            print(f"    Active: {op.par.active}")
else:
    print("  No WebRTC nodes found")

print("\\nLIVEKIT NODES:")
if livekit_ops:
    for op in livekit_ops:
        print(f"  {op.path} ({op.type})")
else:
    print("  No LiveKit nodes found")

print("\\nWEBRENDER NODES:")
if webrender_ops:
    for op in webrender_ops:
        print(f"  {op.path} ({op.type})")
        if hasattr(op.par, 'httpport'):
            print(f"    HTTP Port: {op.par.httpport}")
        if hasattr(op.par, 'active'):
            print(f"    Active: {op.par.active}")
else:
    print("  No WebRender nodes found")

print("\\nNDI NODES:")
if ndi_ops:
    for op in ndi_ops:
        print(f"  {op.path} ({op.type})")
        if hasattr(op.par, 'active'):
            print(f"    Active: {op.par.active}")
        if hasattr(op.par, 'ndiname'):
            print(f"    NDI Name: {op.par.ndiname}")
else:
    print("  No NDI nodes found")

# Check for specific WebRender TOP
print("\\nWEB RENDER TOP CHECK:")
webrender = op('webrender1')
if webrender:
    print(f"  Found at: {webrender.path}")
    print(f"  HTTP Port: {webrender.par.httpport if hasattr(webrender.par, 'httpport') else 'N/A'}")
    print(f"  Active: {webrender.par.active if hasattr(webrender.par, 'active') else 'N/A'}")
else:
    print("  webrender1 not found")

print("="*50)
'''
    
    # Copy code to clipboard and paste
    pyperclip.copy(check_code)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # Execute the code (Ctrl+Enter)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(3)
    
    # Take screenshot of results
    screenshot = pyautogui.screenshot()
    screenshot.save('td_webrtc_diagnosis.png')
    print("Screenshot saved as td_webrtc_diagnosis.png")
    
    # Select all text and copy
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    # Get results from clipboard
    results = pyperclip.paste()
    
    # Save results to file
    with open('td_webrtc_diagnosis.txt', 'w') as f:
        f.write(results)
    
    print("\nDiagnosis results saved to td_webrtc_diagnosis.txt")
    print("\nResults:")
    print(results)
    
    # Close textport
    pyautogui.hotkey('alt', 't')

if __name__ == "__main__":
    check_td_webrtc()
