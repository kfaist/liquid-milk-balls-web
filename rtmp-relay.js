// RTMP Relay: OBS → Node Server → LiveKit
// This solves OBS crashing and gives reliable real-time streaming

const express = require('express');
const { exec } = require('child_process');
const NodeMediaServer = require('node-media-server');

const RTMP_PORT = 1935;

// RTMP Server Config - accepts from OBS, forwards to LiveKit
const config = {
  rtmp: {
    port: RTMP_PORT,
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60
  },
  http: {
    port: 8000,
    allow_origin: '*'
  }
};

const nms = new NodeMediaServer(config);

nms.on('prePublish', (id, StreamPath, args) => {
  console.log('[RTMP] Stream started:', StreamPath);
  console.log('[RTMP] Forwarding to LiveKit...');
  
  // Forward to LiveKit using FFmpeg
  const liveKitRTMP = 'rtmps://claymation-transcription-l6e51sws.livekit.cloud:443/live/processed-output?access_token=YOUR_TOKEN';
  
  const ffmpegCmd = `ffmpeg -re -i rtmp://localhost:${RTMP_PORT}${StreamPath} -c copy -f flv "${liveKitRTMP}"`;
  
  exec(ffmpegCmd, (error, stdout, stderr) => {
    if (error) {
      console.error('[FFmpeg] Error:', error);
    }
  });
});

nms.run();

console.log('='*60);
console.log('RTMP RELAY SERVER RUNNING');
console.log('='*60);
console.log(`\nOBS Configuration:`);
console.log(`  Service: Custom`);
console.log(`  Server: rtmp://localhost:${RTMP_PORT}/live`);
console.log(`  Stream Key: output`);
console.log('\nThis relay forwards OBS → LiveKit for global viewing');
console.log('='*60);
