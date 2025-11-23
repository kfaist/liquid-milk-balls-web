const { IngressClient } = require('livekit-server-sdk');

const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';

async function listIngresses() {
  console.log('Listing all ingresses...\n');
  
  const ingressClient = new IngressClient(
    LIVEKIT_URL.replace('wss://', 'https://'),
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET
  );
  
  try {
    const ingresses = await ingressClient.listIngress();
    
    console.log(`Found ${ingresses.length} ingress(es):\n`);
    
    ingresses.forEach((ingress, index) => {
      console.log(`${index + 1}. Ingress ID: ${ingress.ingressId}`);
      console.log(`   Name: ${ingress.name || '(unnamed)'}`);
      console.log(`   Room: ${ingress.roomName || '(no room)'}`);
      console.log(`   Type: ${ingress.inputType}`);
      console.log(`   State: ${ingress.state?.status || 'unknown'}`);
      console.log(`   URL: ${ingress.url || '(no URL)'}`);
      console.log(`   Stream Key: ${ingress.streamKey ? ingress.streamKey.substring(0, 20) + '...' : '(no key)'}`);
      console.log('');
    });
    
    if (ingresses.length === 0) {
      console.log('No ingresses found. You can create a new one!');
    } else {
      console.log('To delete an ingress, use:');
      console.log('  ingressClient.deleteIngress("ingress-id-here")');
    }
    
    return ingresses;
    
  } catch (error) {
    console.log('ERROR listing ingresses:', error.message);
  }
}

listIngresses();
