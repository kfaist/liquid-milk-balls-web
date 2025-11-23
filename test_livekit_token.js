const { AccessToken } = require('livekit-server-sdk');

const LIVEKIT_API_KEY = 'APITw2Yp2Tv3yfg';
const LIVEKIT_API_SECRET = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';
const PROCESSED_ROOM = 'processed-output';

async function testToken() {
  console.log('Creating fresh LiveKit token...\n');
  
  const token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity: 'obs-processed-output',
    ttl: '2h',
  });

  token.addGrant({
    room: PROCESSED_ROOM,
    roomJoin: true,
    canPublish: true,
    canSubscribe: false,
  });

  const jwt = await token.toJwt();
  const whipUrl = `https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token=${jwt}`;
  
  console.log('Token created successfully!');
  console.log('Room:', PROCESSED_ROOM);
  console.log('Identity: obs-processed-output');
  console.log('\nWHIP URL (first 100 chars):');
  console.log(whipUrl.substring(0, 100) + '...');
  console.log('\nFull WHIP URL length:', whipUrl.length);
  
  // Test if we can actually reach the WHIP endpoint
  console.log('\n\nTesting WHIP endpoint connectivity...');
  try {
    const https = require('https');
    const url = require('url');
    const parsedUrl = url.parse(whipUrl);
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: 'OPTIONS',
      headers: {
        'Origin': 'http://localhost:3000'
      }
    };
    
    const req = https.request(options, (res) => {
      console.log('WHIP endpoint response status:', res.statusCode);
      console.log('Headers:', res.headers);
      if (res.statusCode === 200 || res.statusCode === 204) {
        console.log('\n✓ WHIP endpoint is reachable!');
      } else {
        console.log('\n✗ WHIP endpoint returned unexpected status');
      }
    });
    
    req.on('error', (e) => {
      console.log('✗ Error reaching WHIP endpoint:', e.message);
    });
    
    req.end();
  } catch (err) {
    console.log('Error testing endpoint:', err.message);
  }
}

testToken();
