import socket

# Connect to TouchDesigner textport
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5555))

# Reload webrender with fixed HTML
commands = """
op('/webrender_livekit_input').par.url = 'http://localhost:3000/td-auto-viewer.html'
op('/webrender_livekit_input').par.active = True
op('/webrender_livekit_input').par.reload.pulse()
print("✓ WEBRENDER RELOADED WITH FIXED HTML")
"""

sock.sendall(commands.encode('utf-8'))
response = sock.recv(4096).decode('utf-8')
print(response)

sock.close()
print("\n✅ TouchDesigner webrender reloaded!")
