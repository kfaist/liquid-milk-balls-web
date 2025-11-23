const { IngressClient } = require('livekit-server-sdk');

const LIVEKIT_URL = 'wss://claymation-transcription-l6e51sws.livekit.cloud';
const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';

async function getIngressDetails() {
  console.log('Getting full ingress details...\n');
  
  const ingressClient = new IngressClient(
    LIVEKIT_URL.replace('wss://', 'https://'),
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET
  );
  
  try {
    const ingresses = await ingressClient.listIngress();
    
    if (ingresses.length > 0) {
      const ingress = ingresses[0]; // Use first one
      
      console.log('='.repeat(60));
      console.log('INGRESS CONFIGURATION FOR OBS');
      console.log('='.repeat(60));
      console.log('');
      console.log('Ingress ID:', ingress.ingressId);
      console.log('Name:', ingress.name);
      console.log('Room:', ingress.roomName);
      console.log('');
      console.log('OBS Settings:');
      console.log('  Service: WHIP');
      console.log('  Server:', ingress.url);
      console.log('  Bearer Token:', ingress.streamKey);
      console.log('');
      console.log('='.repeat(60));
      
      // Write to OBS config
      const fs = require('fs');
      const obsConfig = {
        type: "whip_custom",
        settings: {
          server: ingress.url,
          use_auth: false,
          bwtest: false,
          service: "WHIP",
          bearer_token: ingress.streamKey
        }
      };
      
      const configPath = 'C:\\Users\\krista-showputer\\AppData\\Roaming\\obs-studio\\basic\\profiles\\Untitled\\service.json';
      fs.writeFileSync(configPath, JSON.stringify(obsConfig));
      console.log('✓ OBS configuration updated!');
      console.log('✓ Restart OBS and click "Start Streaming"');
      
    } else {
      console.log('No ingresses found.');
    }
    
  } catch (error) {
    console.log('ERROR:', error.message);
  }
}

getIngressDetails();
