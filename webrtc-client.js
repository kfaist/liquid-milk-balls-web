/**
 * WebRTC Client for Mirror's Echo
 * 
 * Integrates with the index.html page via window.MIRRORS_ECHO API
 * Features:
 * - Fetches time-limited TURN credentials from /api/turn-credentials
 * - Uses existing signaling WebSocket at /signaling
 * - Exposes startLocalCamera() and startCall() methods
 * - Attaches local/remote streams to page via window.MIRRORS_ECHO.setLocalStream/setRemoteStream
 * - Handles Connect/Disconnect buttons from index.html
 */

(function() {
  'use strict';

  // Configuration
  const SIGNALING_PATH = '/signaling';
  const TURN_CREDENTIALS_ENDPOINT = '/api/turn-credentials';
  const DEFAULT_ROOM = 'mirrors-echo-default';

  // State
  let localStream = null;
  let peerConnection = null;
  let signalingSocket = null;
  let isInitiator = false;
  let turnCredentials = null;

  // Base WebRTC configuration with public STUN server
  // TURN servers will be added after fetching credentials
  const baseRtcConfig = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' }
    ]
  };

  /**
   * Fetch TURN credentials from server
   * @returns {Promise<Object>} TURN credentials
   */
  async function fetchTurnCredentials() {
    try {
      console.log('[WebRTC] Fetching TURN credentials...');
      const response = await fetch(TURN_CREDENTIALS_ENDPOINT);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch TURN credentials: ${response.statusText}`);
      }

      const credentials = await response.json();
      console.log('[WebRTC] TURN credentials received:', credentials);
      return credentials;
    } catch (error) {
      console.warn('[WebRTC] Failed to fetch TURN credentials, continuing with STUN only:', error);
      return null;
    }
  }

  /**
   * Build RTCPeerConnection configuration with TURN credentials
   * @returns {Object} RTCPeerConnection configuration
   */
  function buildRtcConfig() {
    const config = { ...baseRtcConfig };
    
    if (turnCredentials) {
      // Add TURN servers with credentials
      config.iceServers.push({
        urls: turnCredentials.urls,
        username: turnCredentials.username,
        credential: turnCredentials.credential
      });
      console.log('[WebRTC] Using TURN servers:', turnCredentials.urls);
    } else {
      console.log('[WebRTC] Using STUN servers only (no TURN credentials)');
    }

    return config;
  }

  /**
   * Start local camera and attach to page
   * @returns {Promise<MediaStream>}
   */
  async function startLocalCamera() {
    try {
      console.log('[WebRTC] Starting local camera...');
      
      const constraints = {
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: true
      };

      localStream = await navigator.mediaDevices.getUserMedia(constraints);
      console.log('[WebRTC] Local camera started');

      // Attach to page via MIRRORS_ECHO API
      if (window.MIRRORS_ECHO && window.MIRRORS_ECHO.setLocalStream) {
        window.MIRRORS_ECHO.setLocalStream(localStream);
        console.log('[WebRTC] Local stream attached to page');
      } else {
        console.warn('[WebRTC] window.MIRRORS_ECHO.setLocalStream not available');
      }

      return localStream;
    } catch (error) {
      console.error('[WebRTC] Error starting camera:', error);
      
      // Provide user-friendly error messages
      let message = 'Failed to access camera';
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        message = 'Camera permission denied. Please allow camera access and try again.';
      } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        message = 'No camera found. Please connect a camera and try again.';
      } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
        message = 'Camera is already in use by another application.';
      } else if (error.name === 'NotSupportedError') {
        message = 'Camera access requires HTTPS or localhost.';
      }

      throw new Error(message);
    }
  }

  /**
   * Stop local camera and release resources
   */
  function stopLocalCamera() {
    if (localStream) {
      console.log('[WebRTC] Stopping local camera...');
      localStream.getTracks().forEach(track => track.stop());
      localStream = null;

      // Clear from page
      if (window.MIRRORS_ECHO && window.MIRRORS_ECHO.setLocalStream) {
        window.MIRRORS_ECHO.setLocalStream(null);
      }
      console.log('[WebRTC] Local camera stopped');
    }
  }

  /**
   * Connect to signaling server and start WebRTC call
   * @param {string} room - Room name for signaling
   * @returns {Promise<void>}
   */
  async function startCall(room = DEFAULT_ROOM) {
    if (!localStream) {
      throw new Error('Start camera first');
    }

    try {
      console.log('[WebRTC] Starting call...');

      // Fetch TURN credentials before creating peer connection
      turnCredentials = await fetchTurnCredentials();

      // Connect to signaling server
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const signalingUrl = `${protocol}//${window.location.host}${SIGNALING_PATH}`;
      console.log('[WebRTC] Connecting to signaling server:', signalingUrl);

      signalingSocket = new WebSocket(signalingUrl);

      signalingSocket.onopen = () => {
        console.log('[WebRTC] Connected to signaling server');
        // Join room
        signalingSocket.send(JSON.stringify({ type: 'join', room: room }));
      };

      signalingSocket.onmessage = handleSignalingMessage;

      signalingSocket.onerror = (error) => {
        console.error('[WebRTC] WebSocket error:', error);
        throw new Error('Failed to connect to signaling server');
      };

      signalingSocket.onclose = () => {
        console.log('[WebRTC] Disconnected from signaling server');
      };

    } catch (error) {
      console.error('[WebRTC] Error starting call:', error);
      throw error;
    }
  }

  /**
   * Handle signaling messages
   * @param {MessageEvent} event
   */
  async function handleSignalingMessage(event) {
    try {
      const message = JSON.parse(event.data);
      console.log('[WebRTC] Received signaling message:', message.type);

      switch (message.type) {
        case 'joined':
          console.log('[WebRTC] Successfully joined room:', message.room);
          break;

        case 'ready':
          // We are the initiator, create offer
          console.log('[WebRTC] Ready to create offer');
          isInitiator = true;
          await createPeerConnection();
          await createOffer();
          break;

        case 'offer':
          // We received an offer, create answer
          console.log('[WebRTC] Received offer');
          isInitiator = false;
          await createPeerConnection();
          await handleOffer(message.offer || message.payload);
          break;

        case 'answer':
          // We received an answer to our offer
          console.log('[WebRTC] Received answer');
          await handleAnswer(message.answer || message.payload);
          break;

        case 'candidate':
          // We received an ICE candidate
          await handleCandidate(message.candidate || message.payload);
          break;

        case 'bye':
          // Other peer hung up
          console.log('[WebRTC] Remote peer hung up');
          hangup();
          break;
      }
    } catch (error) {
      console.error('[WebRTC] Error handling signaling message:', error);
    }
  }

  /**
   * Create RTCPeerConnection
   */
  async function createPeerConnection() {
    const config = buildRtcConfig();
    console.log('[WebRTC] Creating peer connection with config:', config);
    
    peerConnection = new RTCPeerConnection(config);

    // Add local stream tracks to peer connection
    if (localStream) {
      localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
        console.log('[WebRTC] Added local track:', track.kind);
      });
    }

    // Handle incoming remote stream
    peerConnection.ontrack = (event) => {
      console.log('[WebRTC] Received remote track:', event.track.kind);
      
      if (event.streams && event.streams[0]) {
        // Attach to page via MIRRORS_ECHO API
        if (window.MIRRORS_ECHO && window.MIRRORS_ECHO.setRemoteStream) {
          window.MIRRORS_ECHO.setRemoteStream(event.streams[0]);
          console.log('[WebRTC] Remote stream attached to page');
        } else {
          console.warn('[WebRTC] window.MIRRORS_ECHO.setRemoteStream not available');
        }
      }
    };

    // Handle ICE candidates
    peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        console.log('[WebRTC] Sending ICE candidate');
        signalingSocket.send(JSON.stringify({
          type: 'candidate',
          candidate: event.candidate
        }));
      }
    };

    // Handle connection state changes
    peerConnection.onconnectionstatechange = () => {
      console.log('[WebRTC] Connection state:', peerConnection.connectionState);
      
      if (peerConnection.connectionState === 'connected') {
        console.log('[WebRTC] ✅ WebRTC connection established');
      } else if (peerConnection.connectionState === 'disconnected' || 
                 peerConnection.connectionState === 'failed') {
        console.warn('[WebRTC] Connection lost or failed');
      }
    };

    // Handle ICE connection state
    peerConnection.oniceconnectionstatechange = () => {
      console.log('[WebRTC] ICE connection state:', peerConnection.iceConnectionState);
    };
  }

  /**
   * Create and send offer
   */
  async function createOffer() {
    try {
      console.log('[WebRTC] Creating offer...');
      const offer = await peerConnection.createOffer();
      await peerConnection.setLocalDescription(offer);

      signalingSocket.send(JSON.stringify({
        type: 'offer',
        offer: offer
      }));

      console.log('[WebRTC] Offer sent');
    } catch (error) {
      console.error('[WebRTC] Error creating offer:', error);
      throw error;
    }
  }

  /**
   * Handle received offer and create answer
   */
  async function handleOffer(offer) {
    try {
      console.log('[WebRTC] Handling offer...');
      await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));

      const answer = await peerConnection.createAnswer();
      await peerConnection.setLocalDescription(answer);

      signalingSocket.send(JSON.stringify({
        type: 'answer',
        answer: answer
      }));

      console.log('[WebRTC] Answer sent');
    } catch (error) {
      console.error('[WebRTC] Error handling offer:', error);
      throw error;
    }
  }

  /**
   * Handle received answer
   */
  async function handleAnswer(answer) {
    try {
      console.log('[WebRTC] Handling answer...');
      await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
      console.log('[WebRTC] Answer processed');
    } catch (error) {
      console.error('[WebRTC] Error handling answer:', error);
      throw error;
    }
  }

  /**
   * Handle received ICE candidate
   */
  async function handleCandidate(candidate) {
    try {
      await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
      console.log('[WebRTC] ICE candidate added');
    } catch (error) {
      console.error('[WebRTC] Error handling ICE candidate:', error);
    }
  }

  /**
   * Hang up call and clean up resources
   */
  function hangup() {
    console.log('[WebRTC] Hanging up...');

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

    // Clear remote stream from page
    if (window.MIRRORS_ECHO && window.MIRRORS_ECHO.setRemoteStream) {
      window.MIRRORS_ECHO.setRemoteStream(null);
    }

    isInitiator = false;
    turnCredentials = null;

    console.log('[WebRTC] Call ended');
  }

  // Initialize when DOM is ready
  function initialize() {
    console.log('[WebRTC] Initializing Mirror\'s Echo WebRTC client...');

    // Check for required APIs
    if (!window.MIRRORS_ECHO) {
      console.error('[WebRTC] window.MIRRORS_ECHO API not found');
      return;
    }

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error('[WebRTC] getUserMedia not supported');
      alert('Your browser does not support camera access. Please use a modern browser with HTTPS.');
      return;
    }

    // Connect to DOM elements
    const connectBtn = document.getElementById('connectBtn');
    const disconnectBtn = document.getElementById('disconnectBtn');

    if (!connectBtn || !disconnectBtn) {
      console.error('[WebRTC] Connect/Disconnect buttons not found in DOM');
      return;
    }

    // Set up event handlers
    connectBtn.addEventListener('click', async () => {
      try {
        connectBtn.disabled = true;
        connectBtn.textContent = 'Connecting...';

        // Start camera if not already started
        if (!localStream) {
          await startLocalCamera();
        }

        // Start call
        await startCall();

        connectBtn.style.display = 'none';
        disconnectBtn.style.display = 'inline-block';
        disconnectBtn.disabled = false;

        console.log('[WebRTC] Connected successfully');
      } catch (error) {
        console.error('[WebRTC] Connection failed:', error);
        alert(`Connection failed: ${error.message}`);
        connectBtn.disabled = false;
        connectBtn.textContent = 'Connect';
      }
    });

    disconnectBtn.addEventListener('click', () => {
      hangup();
      stopLocalCamera();

      connectBtn.style.display = 'inline-block';
      connectBtn.disabled = false;
      connectBtn.textContent = 'Connect';
      disconnectBtn.style.display = 'none';

      console.log('[WebRTC] Disconnected');
    });

    // Initial button states
    disconnectBtn.style.display = 'none';

    console.log('[WebRTC] Initialization complete');
  }

  // Run initialization when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }

  // Expose API for programmatic control
  window.MirrorsEchoWebRTC = {
    startLocalCamera,
    stopLocalCamera,
    startCall,
    hangup,
    getLocalStream: () => localStream,
    getPeerConnection: () => peerConnection
  };

})();
