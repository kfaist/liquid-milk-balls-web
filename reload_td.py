"""
TouchDesigner WebRender Reloader
Connects to TD textport and reloads the webrender operator
"""

import socket
import time

print("Connecting to TouchDesigner textport...")

try:
    # Connect to TouchDesigner textport (default port 5555)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(('localhost', 5555))
    print("[OK] Connected to TouchDesigner")
    
    # Commands to reload webrender
    commands = """
op('/webrender_livekit_input').par.url = 'http://localhost:3000/td-auto-viewer.html'
op('/webrender_livekit_input').par.active = True
op('/webrender_livekit_input').par.reload.pulse()
print("WEBRENDER RELOADED")
"""
    
    # Send commands
    sock.sendall(commands.encode('utf-8'))
    print("[OK] Commands sent to TouchDesigner")
    
    # Wait for response
    time.sleep(1)
    try:
        response = sock.recv(4096).decode('utf-8')
        if response:
            print(f"[RESPONSE] {response}")
    except:
        pass
    
    sock.close()
    print("[SUCCESS] WebRender reload command sent!")
    print("\nNow check TouchDesigner webrender_livekit_input operator")
    print("You should see it loading the td-auto-viewer.html page")
    
except ConnectionRefusedError:
    print("[ERROR] Cannot connect to TouchDesigner textport")
    print("Make sure:")
    print("1. TouchDesigner is running")
    print("2. Textport is enabled (Edit > Preferences > Network)")
    print("3. Port 5555 is open")
    print("\nALTERNATIVE: Manually paste this in TD Textport:")
    print("op('/webrender_livekit_input').par.reload.pulse()")
    
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nMANUAL OPTION: Open TD Textport (Alt+T) and paste:")
    print("op('/webrender_livekit_input').par.reload.pulse()")
