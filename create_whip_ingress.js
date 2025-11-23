const { IngressClient, IngressInput } = require('livekit-server-sdk');

const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const ROOM_NAME = 'processed-output';

async function createWHIPIngress() {
  console.log('Creating WHIP Ingress for LiveKit...\n');
  
  const ingressClient = new IngressClient(
    LIVEKIT_URL.replace('wss://', 'https://'),
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET
  );
  
  try {
    const ingress = await ingressClient.createIngress(
      IngressInput.WHIP_INPUT,
      {
        name: 'OBS-Processed-Output',
        roomName: ROOM_NAME,
        participantIdentity: 'obs-processed-stream',
        participantName: 'OBS-Stream',
      }
    );
    
    console.log('SUCCESS! WHIP Ingress created!\n');
    console.log('Ingress ID:', ingress.ingressId);
    console.log('Stream Key:', ingress.streamKey);
    console.log('URL:', ingress.url);
    
    console.log('\n' + '='.repeat(60));
    console.log('CONFIGURE OBS WITH THESE VALUES:');
    console.log('='.repeat(60));
    console.log('Service: WHIP');
    console.log('Server:', ingress.url);
    console.log('Bearer Token:', ingress.streamKey);
    console.log('='.repeat(60));
    
    return ingress;
    
  } catch (error) {
    console.log('ERROR creating ingress:', error.message);
    
    if (error.code === 12 || error.message.includes('Unimplemented') || error.message.includes('not implemented')) {
      console.log('\n' + '='.repeat(60));
      console.log('CRITICAL FINDING:');
      console.log('='.repeat(60));
      console.log('LiveKit Cloud does NOT support Ingress API');
      console.log('Error code 12 = Unimplemented');
      console.log('\nThis confirms WHIP ingress is NOT available on your LiveKit Cloud plan.');
      console.log('\nYou need to EITHER:');
      console.log('1. Upgrade to a LiveKit plan that includes Ingress support');
      console.log('2. Use a different architecture (remove OBS from pipeline)');
      console.log('='.repeat(60));
    } else if (error.message.includes('permission') || error.message.includes('unauthorized')) {
      console.log('\nAPI keys may not have ingress permissions');
      console.log('Check your LiveKit Cloud project settings');
    } else {
      console.log('\nFull error details:', error);
    }
  }
}

createWHIPIngress();
