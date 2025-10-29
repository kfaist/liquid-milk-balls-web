// WebRTC Signaling Server for local testing
// A minimal signaling relay using WebSocket (ws library)
// WARNING: This is an insecure relay intended only for local testing

const WebSocket = require('ws');

const PORT = process.env.PORT || 8888;
const wss = new WebSocket.Server({ port: PORT });

// Store connected clients
const clients = new Set();

console.log(`WebRTC Signaling Server started on ws://localhost:${PORT}`);
console.log('Waiting for clients to connect...');

wss.on('connection', (ws) => {
    console.log('New client connected. Total clients:', clients.size + 1);
    
    // Add client to set
    clients.add(ws);
    
    ws.on('message', (message) => {
        let data;
        try {
            data = JSON.parse(message);
        } catch (error) {
            console.error('Invalid JSON received:', error);
            return;
        }
        
        console.log('Received message type:', data.type);
        
        // Handle different message types
        switch (data.type) {
            case 'join':
                // When a client joins, check if there's another client waiting
                if (clients.size >= 2) {
                    // Signal the new client that another peer is ready
                    ws.send(JSON.stringify({ type: 'ready' }));
                }
                break;
                
            case 'offer':
            case 'answer':
            case 'candidate':
            case 'bye':
                // Relay message to all other clients
                clients.forEach(client => {
                    if (client !== ws && client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(data));
                    }
                });
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    });
    
    ws.on('close', () => {
        console.log('Client disconnected. Total clients:', clients.size - 1);
        clients.delete(ws);
        
        // Notify other clients that peer left
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ type: 'bye' }));
            }
        });
    });
    
    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
    });
});

wss.on('error', (error) => {
    console.error('Server error:', error);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down signaling server...');
    
    // Close all client connections
    clients.forEach(client => {
        client.close();
    });
    
    // Close server
    wss.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});

console.log('\nUsage:');
console.log('1. Start this signaling server: node webrtc-signaling-server.js');
console.log('2. Open index.html in a browser at http://localhost:8000');
console.log('3. Click "Start Camera" and then "Start WebRTC Call"');
console.log('4. Open another browser tab/window and repeat step 3');
console.log('\nPress Ctrl+C to stop the server');
