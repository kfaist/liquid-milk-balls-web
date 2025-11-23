const { AccessToken, RoomServiceClient } = require('livekit-server-sdk');

const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const PROCESSED_ROOM = 'processed-output';

async function createIngress() {
  console.log('Connecting to LiveKit...\n');
  
  const roomService = new RoomServiceClient(
    LIVEKIT_URL.replace('wss://', 'https://'),
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET
  );
  
  try {
    // Check if room exists
    console.log(`Checking if room "${PROCESSED_ROOM}" exists...`);
    const rooms = await roomService.listRooms([PROCESSED_ROOM]);
    console.log('Rooms found:', rooms.length);
    
    if (rooms.length === 0) {
      console.log(`Room "${PROCESSED_ROOM}" does not exist yet - it will be created when first publisher connects\n`);
    } else {
      console.log(`Room "${PROCESSED_ROOM}" exists!`);
      console.log('Room details:', JSON.stringify(rooms[0], null, 2));
    }
    
    // Create WHIP ingress
    console.log('\nNOTE: LiveKit Cloud does NOT support Ingress creation via API');
    console.log('WHIP ingress is managed automatically by LiveKit Cloud');
    console.log('\nFor LiveKit Cloud, use WHIP URL directly:');
    console.log('https://<your-cloud>.livekit.cloud/whip?access_token=<token>');
    
  } catch (error) {
    console.log('Error:', error.message);
    
    if (error.message.includes('Unimplemented')) {
      console.log('\n✓ This is expected for LiveKit Cloud!');
      console.log('LiveKit Cloud does not support Ingress API');
      console.log('Instead, use the WHIP URL format directly');
    }
  }
}

createIngress();
