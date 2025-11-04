// LiveKit Publisher Client - Publishes camera to LiveKit room
// Uses same UI as custom WebRTC but connects to LiveKit backend
// Compatible with ndi-viewer.html for OBS consumption

(function() {
    'use strict';
    
    // Wait for DOM to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    function init() {
        // Check if LiveKit SDK is available
        const maxRetries = 10;
        let retryCount = 0;
        
        function checkLiveKit() {
            if (typeof window.LivekitClient !== 'undefined') {
                console.log('✅ LiveKit SDK loaded successfully');
                initPublisher(window.LivekitClient);
            } else if (retryCount < maxRetries) {
                retryCount++;
                console.log(`⏳ Waiting for LiveKit SDK... (attempt ${retryCount}/${maxRetries})`);
                setTimeout(checkLiveKit, 200);
            } else {
                console.error('❌ LiveKit SDK failed to load after', maxRetries, 'attempts');
                const statusText = document.getElementById('statusText');
                if (statusText) {
                    statusText.textContent = '❌ Error: LiveKit SDK not loaded. Please refresh the page.';
                }
            }
        }
        
        checkLiveKit();
    }
    
    function initPublisher(LivekitClient) {
        console.log('🎬 Initializing LiveKit Publisher...');
        
        // DOM elements
        const localVideo = document.getElementById('localVideo');
        const remoteVideo = document.getElementById('remoteVideo');
        const startCameraBtn = document.getElementById('startCameraBtn');
        const stopCameraBtn = document.getElementById('stopCameraBtn');
        const startCallBtn = document.getElementById('startCallBtn');
        const hangupBtn = document.getElementById('hangupBtn');
        const statusText = document.getElementById('statusText');
        
        // LiveKit state
        let localStream = null;
        let room = null;
        let connected = false;
        
        // Button event listeners
        if (startCameraBtn) startCameraBtn.addEventListener('click', startCamera);
        if (stopCameraBtn) stopCameraBtn.addEventListener('click', stopCamera);
        if (startCallBtn) startCallBtn.addEventListener('click', startCall);
        if (hangupBtn) hangupBtn.addEventListener('click', hangup);
        
        const ndiBtn = document.getElementById('ndiBtn');
        if (ndiBtn) {
            ndiBtn.addEventListener('click', enableNDI);
        }
        
        // Start camera using getUserMedia
        async function startCamera() {
            try {
                updateStatus('Requesting camera access...');
                
                const constraints = {
                    video: {
                        width: { ideal: 1920 },
                        height: { ideal: 1080 }
                    },
                    audio: true
                };
                
                localStream = await navigator.mediaDevices.getUserMedia(constraints);
                localVideo.srcObject = localStream;
                
                updateStatus('Camera started - Ready to connect to LiveKit');
                updateButtonStates('cameraStarted');
                
            } catch (error) {
                console.error('Error accessing camera:', error);
                let errorMessage = 'Error: Could not access camera';
                
                if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                    errorMessage = 'Error: Camera permission denied. Please allow camera access and try again.';
                } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
                    errorMessage = 'Error: No camera found. Please connect a camera and try again.';
                } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
                    errorMessage = 'Error: Camera is already in use by another application.';
                } else if (error.name === 'OverconstrainedError' || error.name === 'ConstraintNotSatisfiedError') {
                    errorMessage = 'Error: Camera does not support the requested settings.';
                } else if (error.name === 'NotSupportedError') {
                    errorMessage = 'Error: Camera access is not supported. Please use HTTPS.';
                } else {
                    errorMessage = 'Error: ' + error.message;
                }
                
                updateStatus(errorMessage);
            }
        }
        
        // Stop camera
        function stopCamera() {
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
                localVideo.srcObject = null;
                localStream = null;
                
                updateStatus('Camera stopped');
                updateButtonStates('cameraStopped');
                
                if (room) {
                    hangup();
                }
            }
        }
        
        // Connect to LiveKit and publish camera
        async function startCall() {
            if (!localStream) {
                updateStatus('Error: Start camera first');
                return;
            }
            
            try {
                updateStatus('🔄 Getting LiveKit access token...');
                
                // Get publisher token from server
                const response = await fetch('/api/publisher-token');
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Failed to get LiveKit token: ${response.status} - ${errorText}`);
                }
                
                const data = await response.json();
                console.log('📋 Token received for room:', data.roomName);
                
                updateStatus('🔄 Connecting to LiveKit room...');
                
                // Create LiveKit room
                room = new LivekitClient.Room({
                    adaptiveStream: true,
                    dynacast: true,
                    videoCaptureDefaults: {
                        resolution: LivekitClient.VideoPresets.h1080.resolution,
                    }
                });
                
                // Set up event handlers
                room.on(LivekitClient.RoomEvent.Connected, () => {
                    connected = true;
                    updateStatus('✅ Connected to LiveKit room: ' + data.roomName);
                    console.log('✅ Connected to room:', data.roomName);
                });
                
                room.on(LivekitClient.RoomEvent.Disconnected, () => {
                    if (connected) {
                        updateStatus('❌ Disconnected from LiveKit');
                        handleDisconnect();
                    }
                });
                
                room.on(LivekitClient.RoomEvent.ParticipantConnected, (participant) => {
                    console.log('👥 Participant joined:', participant.identity);
                    updateStatus('👥 Viewer joined - Your camera is now being watched!');
                });
                
                room.on(LivekitClient.RoomEvent.ParticipantDisconnected, (participant) => {
                    console.log('👋 Participant left:', participant.identity);
                    updateStatus('👋 Viewer left the room');
                });
                
                // Connect to room
                await room.connect(data.url, data.token);
                
                // Publish camera and microphone
                updateStatus('📹 Publishing camera and microphone...');
                
                const videoTrack = localStream.getVideoTracks()[0];
                const audioTrack = localStream.getAudioTracks()[0];
                
                await room.localParticipant.publishTrack(videoTrack, {
                    name: 'camera',
                    simulcast: true,
                });
                
                if (audioTrack) {
                    await room.localParticipant.publishTrack(audioTrack, {
                        name: 'microphone',
                    });
                }
                
                updateStatus('🎥 Live! Your camera is streaming to OBS via LiveKit');
                updateButtonStates('callStarted');
                
            } catch (error) {
                console.error('❌ Error connecting to LiveKit:', error);
                updateStatus('❌ Error: ' + error.message);
                
                if (room) {
                    room.disconnect();
                    room = null;
                }
            }
        }
        
        // Disconnect from LiveKit
        async function hangup() {
            if (room) {
                updateStatus('Disconnecting from LiveKit...');
                
                // Unpublish tracks
                if (room.localParticipant) {
                    room.localParticipant.tracks.forEach((publication) => {
                        if (publication.track) {
                            room.localParticipant.unpublishTrack(publication.track);
                        }
                    });
                }
                
                await room.disconnect();
                room = null;
            }
            
            connected = false;
            updateStatus('👋 Disconnected from LiveKit');
            updateButtonStates('callEnded');
        }
        
        // Handle unexpected disconnect
        function handleDisconnect() {
            room = null;
            connected = false;
            updateButtonStates('callEnded');
        }
        
        // Update button states
        function updateButtonStates(state) {
            const ndiBtn = document.getElementById('ndiBtn');
            
            switch (state) {
                case 'cameraStarted':
                    if (startCameraBtn) startCameraBtn.disabled = true;
                    if (stopCameraBtn) stopCameraBtn.disabled = false;
                    if (startCallBtn) startCallBtn.disabled = false;
                    if (hangupBtn) hangupBtn.disabled = true;
                    if (ndiBtn) ndiBtn.disabled = false;
                    break;
                    
                case 'cameraStopped':
                    if (startCameraBtn) startCameraBtn.disabled = false;
                    if (stopCameraBtn) stopCameraBtn.disabled = true;
                    if (startCallBtn) startCallBtn.disabled = true;
                    if (hangupBtn) hangupBtn.disabled = true;
                    if (ndiBtn) ndiBtn.disabled = true;
                    break;
                    
                case 'callStarted':
                    if (startCameraBtn) startCameraBtn.disabled = true;
                    if (stopCameraBtn) stopCameraBtn.disabled = true;
                    if (startCallBtn) startCallBtn.disabled = true;
                    if (hangupBtn) hangupBtn.disabled = false;
                    if (ndiBtn) ndiBtn.disabled = false;
                    break;
                    
                case 'callEnded':
                    if (startCameraBtn) startCameraBtn.disabled = true;
                    if (stopCameraBtn) stopCameraBtn.disabled = false;
                    if (startCallBtn) startCallBtn.disabled = false;
                    if (hangupBtn) hangupBtn.disabled = true;
                    if (ndiBtn) ndiBtn.disabled = false;
                    break;
            }
        }
        
        // Enable NDI output (informational)
        function enableNDI() {
            const instructions = `
🎥 NDI Output via LiveKit

Your camera is now streaming through LiveKit!

To capture in OBS:
1. Add a Browser Source in OBS
2. URL: ${window.location.origin}/ndi-viewer.html
3. Width: 1920, Height: 1080
4. Enable "Shutdown source when not visible"

Then in OBS:
• Tools → NDI Output Settings
• Enable "Main Output"

In TouchDesigner:
• Add NDI In TOP
• Select your OBS NDI source
• Process the live stream!

Your remote camera → LiveKit → OBS Browser Source → NDI → TouchDesigner
            `.trim();
            
            console.log(instructions);
            alert(instructions);
        }
        
        // Update status text
        function updateStatus(message) {
            console.log('📊 Status:', message);
            if (statusText) {
                statusText.textContent = message;
            }
        }
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (room) {
                room.disconnect();
            }
        });
        
        console.log('✅ LiveKit Publisher initialized successfully');
        updateStatus('Ready to start - LiveKit enabled');
    }
})();
