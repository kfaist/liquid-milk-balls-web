const { RoomServiceClient, AccessToken } = require('livekit-server-sdk');

const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const ROOM_NAME = 'processed-output';

async function createRoomFirst() {
  console.log('Creating room explicitly before OBS streams...\n');
  
  const roomService = new RoomServiceClient(
    LIVEKIT_URL.replace('wss://', 'https://'),
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET
  );
  
  try {
    // Create room
    const room = await roomService.createRoom({
      name: ROOM_NAME,
      emptyTimeout: 300, // 5 minutes
      maxParticipants: 100,
    });
    
    console.log('✓ Room created successfully!');
    console.log('Room name:', room.name);
    console.log('Room SID:', room.sid);
    console.log('\nNow OBS can stream to this room!');
    
  } catch (error) {
    if (error.message.includes('already exists')) {
      console.log('✓ Room already exists - this is fine!');
      
      // List the room to confirm
      const rooms = await roomService.listRooms([ROOM_NAME]);
      if (rooms.length > 0) {
        console.log('\nExisting room details:');
        console.log('Name:', rooms[0].name);
        console.log('SID:', rooms[0].sid);
        console.log('Participants:', rooms[0].numParticipants);
      }
    } else {
      console.log('✗ Error creating room:', error.message);
    }
  }
}

createRoomFirst();
