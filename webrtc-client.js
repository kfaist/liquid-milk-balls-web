// WebRTC Client for local testing with signaling server
// Implements getUserMedia, WebRTC connection, and simple UI state management

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const localVideo = document.getElementById('localVideo');
    const remoteVideo = document.getElementById('remoteVideo');
    const startCameraBtn = document.getElementById('startCameraBtn');
    const stopCameraBtn = document.getElementById('stopCameraBtn');
    const startCallBtn = document.getElementById('startCallBtn');
    const hangupBtn = document.getElementById('hangupBtn');
    const statusText = document.getElementById('statusText');
    
    // WebRTC state
    let localStream = null;
    let peerConnection = null;
    let signalingSocket = null;
    let isInitiator = false;
    
    // WebRTC configuration with STUN server
    const rtcConfig = {
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' }
        ]
    };
    
    // Signaling server URL
    const SIGNALING_SERVER_URL = 'ws://localhost:8888';
    
    // Button event listeners
    startCameraBtn.addEventListener('click', startCamera);
    stopCameraBtn.addEventListener('click', stopCamera);
    startCallBtn.addEventListener('click', startCall);
    hangupBtn.addEventListener('click', hangup);
    
    // Start camera using getUserMedia
    async function startCamera() {
        try {
            updateStatus('Requesting camera access...');
            
            const constraints = {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: true
            };
            
            localStream = await navigator.mediaDevices.getUserMedia(constraints);
            localVideo.srcObject = localStream;
            
            updateStatus('Camera started');
            updateButtonStates('cameraStarted');
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            let errorMessage = 'Error: Could not access camera';
            
            // Provide more specific error messages
            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                errorMessage = 'Error: Camera permission denied. Please allow camera access and try again.';
            } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
                errorMessage = 'Error: No camera found. Please connect a camera and try again.';
            } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
                errorMessage = 'Error: Camera is already in use by another application.';
            } else if (error.name === 'OverconstrainedError' || error.name === 'ConstraintNotSatisfiedError') {
                errorMessage = 'Error: Camera does not support the requested settings.';
            } else if (error.name === 'NotSupportedError') {
                errorMessage = 'Error: Camera access is not supported in this browser. Please use HTTPS or localhost.';
            } else {
                errorMessage = 'Error: ' + error.message;
            }
            
            updateStatus(errorMessage);
        }
    }
    
    // Stop camera and release media devices
    function stopCamera() {
        if (localStream) {
            localStream.getTracks().forEach(track => track.stop());
            localVideo.srcObject = null;
            localStream = null;
            
            updateStatus('Camera stopped');
            updateButtonStates('cameraStopped');
            
            // Also hangup if there's an active call
            if (peerConnection) {
                hangup();
            }
        }
    }
    
    // Start WebRTC call
    async function startCall() {
        if (!localStream) {
            updateStatus('Error: Start camera first');
            return;
        }
        
        try {
            updateStatus('Connecting to signaling server...');
            
            // Connect to signaling server
            signalingSocket = new WebSocket(SIGNALING_SERVER_URL);
            
            signalingSocket.onopen = () => {
                updateStatus('Connected to signaling server');
                // Send join message
                signalingSocket.send(JSON.stringify({ type: 'join' }));
            };
            
            signalingSocket.onmessage = handleSignalingMessage;
            
            signalingSocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                updateStatus('Error: Could not connect to signaling server at ' + SIGNALING_SERVER_URL + '. Make sure the server is running.');
            };
            
            signalingSocket.onclose = () => {
                updateStatus('Disconnected from signaling server');
            };
            
            updateButtonStates('callStarted');
            
        } catch (error) {
            console.error('Error starting call:', error);
            updateStatus('Error: ' + error.message);
        }
    }
    
    // Handle signaling messages
    async function handleSignalingMessage(event) {
        const message = JSON.parse(event.data);
        
        console.log('Received signaling message:', message.type);
        
        switch (message.type) {
            case 'ready':
                // We are the initiator, create offer
                isInitiator = true;
                await createPeerConnection();
                await createOffer();
                break;
                
            case 'offer':
                // We received an offer, create answer
                isInitiator = false;
                await createPeerConnection();
                await handleOffer(message.offer);
                break;
                
            case 'answer':
                // We received an answer to our offer
                await handleAnswer(message.answer);
                break;
                
            case 'candidate':
                // We received an ICE candidate
                await handleCandidate(message.candidate);
                break;
                
            case 'bye':
                // Other peer hung up
                handleRemoteHangup();
                break;
        }
    }
    
    // Create peer connection
    async function createPeerConnection() {
        peerConnection = new RTCPeerConnection(rtcConfig);
        
        // Add local stream tracks to peer connection
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });
        
        // Handle incoming remote stream
        peerConnection.ontrack = (event) => {
            console.log('Received remote track');
            if (remoteVideo.srcObject !== event.streams[0]) {
                remoteVideo.srcObject = event.streams[0];
                updateStatus('Receiving remote stream');
            }
        };
        
        // Handle ICE candidates
        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                console.log('Sending ICE candidate');
                signalingSocket.send(JSON.stringify({
                    type: 'candidate',
                    candidate: event.candidate
                }));
            }
        };
        
        // Handle connection state changes
        peerConnection.onconnectionstatechange = () => {
            console.log('Connection state:', peerConnection.connectionState);
            updateStatus('Connection state: ' + peerConnection.connectionState);
            
            if (peerConnection.connectionState === 'connected') {
                updateStatus('WebRTC call connected');
            } else if (peerConnection.connectionState === 'disconnected' || 
                       peerConnection.connectionState === 'failed') {
                updateStatus('Connection lost');
            }
        };
    }
    
    // Create and send offer
    async function createOffer() {
        try {
            updateStatus('Creating offer...');
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            
            signalingSocket.send(JSON.stringify({
                type: 'offer',
                offer: offer
            }));
            
            updateStatus('Offer sent');
        } catch (error) {
            console.error('Error creating offer:', error);
            updateStatus('Error creating offer: ' + error.message);
        }
    }
    
    // Handle received offer and create answer
    async function handleOffer(offer) {
        try {
            updateStatus('Received offer, creating answer...');
            await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
            
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            
            signalingSocket.send(JSON.stringify({
                type: 'answer',
                answer: answer
            }));
            
            updateStatus('Answer sent');
        } catch (error) {
            console.error('Error handling offer:', error);
            updateStatus('Error handling offer: ' + error.message);
        }
    }
    
    // Handle received answer
    async function handleAnswer(answer) {
        try {
            updateStatus('Received answer');
            await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
        } catch (error) {
            console.error('Error handling answer:', error);
            updateStatus('Error handling answer: ' + error.message);
        }
    }
    
    // Handle received ICE candidate
    async function handleCandidate(candidate) {
        try {
            await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
        } catch (error) {
            console.error('Error handling ICE candidate:', error);
        }
    }
    
    // Handle remote hangup
    function handleRemoteHangup() {
        updateStatus('Remote peer hung up');
        hangup();
    }
    
    // Hang up call
    function hangup() {
        // Close peer connection
        if (peerConnection) {
            peerConnection.close();
            peerConnection = null;
        }
        
        // Close signaling socket
        if (signalingSocket) {
            signalingSocket.send(JSON.stringify({ type: 'bye' }));
            signalingSocket.close();
            signalingSocket = null;
        }
        
        // Clear remote video
        remoteVideo.srcObject = null;
        
        updateStatus('Call ended');
        updateButtonStates('callEnded');
    }
    
    // Update button states based on current state
    function updateButtonStates(state) {
        switch (state) {
            case 'cameraStarted':
                startCameraBtn.disabled = true;
                stopCameraBtn.disabled = false;
                startCallBtn.disabled = false;
                hangupBtn.disabled = true;
                break;
                
            case 'cameraStopped':
                startCameraBtn.disabled = false;
                stopCameraBtn.disabled = true;
                startCallBtn.disabled = true;
                hangupBtn.disabled = true;
                break;
                
            case 'callStarted':
                startCameraBtn.disabled = true;
                stopCameraBtn.disabled = true;
                startCallBtn.disabled = true;
                hangupBtn.disabled = false;
                break;
                
            case 'callEnded':
                startCameraBtn.disabled = true;
                stopCameraBtn.disabled = false;
                startCallBtn.disabled = false;
                hangupBtn.disabled = true;
                break;
        }
    }
    
    // Update status text
    function updateStatus(message) {
        console.log('Status:', message);
        statusText.textContent = message;
    }
});
