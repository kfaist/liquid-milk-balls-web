const https = require('https');

const whipUrl = 'https://claymation-transcription-l6e51sws.livekit.cloud/whip?access_token=eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoicHJvY2Vzc2VkLW91dHB1dCIsInJvb21Kb2luIjp0cnVlLCJjYW5QdWJsaXNoIjp0cnVlLCJjYW5TdWJzY3JpYmUiOmZhbHNlfSwiaXNzIjoiQVBJVHcyWXAyVHYzeWZnIiwiZXhwIjoxNzYzODgxNTYzLCJuYmYiOjAsInN1YiI6Im9icy1wcm9jZXNzZWQtb3V0cHV0In0.YWxIGPwqD-quYdmioKnjzbVI7f_b-o6Pf_WDU9jJuT0';

// Test SDP
const testSdp = `v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
m=video 9 UDP/TLS/RTP/SAVPF 96
a=rtpmap:96 H264/90000
a=sendonly`;

const url = new URL(whipUrl);

const options = {
  hostname: url.hostname,
  path: url.pathname + url.search,
  method: 'POST',
  headers: {
    'Content-Type': 'application/sdp',
    'Content-Length': Buffer.byteLength(testSdp)
  }
};

console.log('Testing WHIP POST to:', url.hostname + url.pathname);
console.log('Token length:', url.search.length);

const req = https.request(options, (res) => {
  console.log('\nResponse status:', res.statusCode);
  console.log('Response headers:', res.headers);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('\nResponse body:', data);
    if (res.statusCode === 201) {
      console.log('\n✓ WHIP connection would succeed!');
      console.log('LiveKit is accepting connections to the processed-output room');
    } else if (res.statusCode === 200) {
      console.log('\n! Got 200 instead of 201');
      console.log('This might indicate an issue with the SDP format');
    } else {
      console.log('\n✗ WHIP connection failed');
    }
  });
});

req.on('error', (e) => {
  console.error('✗ Request error:', e.message);
});

req.write(testSdp);
req.end();
