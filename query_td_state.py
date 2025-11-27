"""
Query TouchDesigner state via TDAbleton socket on port 9000
"""
import socket
import json

def query_td():
    try:
        # Connect to TD's socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('127.0.0.1', 9000))
        
        # Send query for all TOPs
        sock.send(b'op("/*").ops')
        response = sock.recv(4096)
        print(f"Response: {response}")
        sock.close()
        return response
    except Exception as e:
        print(f"Socket failed: {e}")
        return None

# Try to just get TD info via pyautogui screenshot
import subprocess

# Take a screenshot of the entire desktop
result = subprocess.run(['powershell', '-Command', 
    'Add-Type -AssemblyName System.Windows.Forms; ' +
    '[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height'],
    capture_output=True, text=True)
print(f"Screen: {result.stdout}")

if __name__ == "__main__":
    query_td()
