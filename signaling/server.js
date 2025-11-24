// Simple WebSocket signaling server for Mirror's Echo
// Usage: PORT=3000 node server.js
const WebSocket = require('ws');

const port = process.env.PORT || 3000;
const wss = new WebSocket.Server({ port });

/*
Protocol (JSON messages):
- join: { type: 'join', role: 'sender'|'receiver', room: '<roomId>' }
- offer: { type: 'offer', room, payload: <RTCSessionDescription> }
- answer: { type: 'answer', room, payload: <RTCSessionDescription> }
- candidate: { type: 'candidate', room, payload: <RTCIceCandidate> }
The server simply forwards messages to other clients in the same room (except sender).
*/

const rooms = new Map(); // roomId => Set of clients {ws, role}

function addToRoom(roomId, clientObj) {
  if (!rooms.has(roomId)) rooms.set(roomId, new Set());
  rooms.get(roomId).add(clientObj);
}

function removeFromRoom(roomId, clientObj) {
  if (!rooms.has(roomId)) return;
  rooms.get(roomId).delete(clientObj);
  if (rooms.get(roomId).size === 0) rooms.delete(roomId);
}

wss.on('connection', function connection(ws) {
  const client = { ws, role: null, room: null };

  ws.on('message', function incoming(message) {
    let msg;
    try { msg = JSON.parse(message); } catch (e) { return; }

    const { type, room, role, payload } = msg;

    if (type === 'join') {
      client.role = role || 'receiver';
      client.room = room || 'mirrors-echo-room';
      addToRoom(client.room, client);
      ws.send(JSON.stringify({ type: 'joined', room: client.room, role: client.role }));
      console.log(`Client joined room=${client.room} role=${client.role} clients=${rooms.get(client.room).size}`);
      return;
    }

    // For signaling messages, forward to other peers in same room
    if (room && rooms.has(room)) {
      for (const other of rooms.get(room)) {
        if (other.ws === ws) continue; // don't echo back
        try {
          other.ws.send(JSON.stringify({ type, room, payload, fromRole: client.role }));
        } catch (e) {
          console.warn('Failed to forward message', e);
        }
      }
    }
  });

  ws.on('close', function () {
    if (client.room) {
      removeFromRoom(client.room, client);
      console.log(`Client left room=${client.room}`);
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err);
  });
});

console.log(`Signaling server running on ws://0.0.0.0:${port}`);