/**
 * LiveKit Join Client
 * 
 * Minimal client snippet to fetch a LiveKit token and connect to a room.
 * 
 * Usage:
 * 1. Include livekit-client in your page:
 *    <script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.min.js"></script>
 * 
 * 2. Call joinLiveKitRoom:
 *    const room = await joinLiveKitRoom('test-room', 'Alice');
 * 
 * 3. Handle events:
 *    room.on('participantConnected', participant => { ... });
 */

/**
 * Fetch a LiveKit token from the server
 * 
 * @param {string} roomName - Room to join
 * @param {string} username - Display name (optional)
 * @param {string} authToken - Your auth token (JWT, session token, etc.)
 * @returns {Promise<object>} - { token, url, room, identity }
 */
async function fetchLiveKitToken(roomName, username = null, authToken = null) {
  try {
    const response = await fetch('/api/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken || 'stub-token'}`,
      },
      body: JSON.stringify({
        room: roomName,
        username: username,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to fetch token');
    }

    return await response.json();
  } catch (error) {
    console.error('[LiveKit] Failed to fetch token:', error);
    throw error;
  }
}

/**
 * Join a LiveKit room
 * 
 * @param {string} roomName - Room to join
 * @param {string} username - Display name (optional)
 * @param {string} authToken - Your auth token (optional, uses stub for testing)
 * @returns {Promise<Room>} - LiveKit Room instance
 */
async function joinLiveKitRoom(roomName, username = null, authToken = null) {
  try {
    // Fetch token from server
    const { token, url } = await fetchLiveKitToken(roomName, username, authToken);

    // Create room instance
    const room = new LivekitClient.Room({
      adaptiveStream: true,
      dynacast: true,
    });

    // Set up event listeners
    room.on('participantConnected', (participant) => {
      console.log('[LiveKit] Participant connected:', participant.identity);
    });

    room.on('participantDisconnected', (participant) => {
      console.log('[LiveKit] Participant disconnected:', participant.identity);
    });

    room.on('trackSubscribed', (track, publication, participant) => {
      console.log('[LiveKit] Track subscribed:', track.kind, 'from', participant.identity);
      
      // Auto-attach video/audio to DOM
      if (track.kind === 'video' || track.kind === 'audio') {
        const element = track.attach();
        document.body.appendChild(element);
      }
    });

    room.on('disconnected', () => {
      console.log('[LiveKit] Disconnected from room');
    });

    // Connect to room
    await room.connect(url, token);
    console.log('[LiveKit] Connected to room:', room.name);

    return room;

  } catch (error) {
    console.error('[LiveKit] Failed to join room:', error);
    throw error;
  }
}

/**
 * Publish camera and microphone to the room
 * 
 * NOTE: This requires canPublish: true in the token
 * In production, verify user subscription/billing before enabling
 * 
 * @param {Room} room - LiveKit Room instance
 * @returns {Promise<void>}
 */
async function publishMediaTracks(room) {
  try {
    // Request camera and microphone permissions
    await room.localParticipant.enableCameraAndMicrophone();
    console.log('[LiveKit] Camera and microphone enabled');
  } catch (error) {
    console.error('[LiveKit] Failed to enable camera/mic:', error);
    throw error;
  }
}

/**
 * Example usage:
 * 
 * // Basic join (view-only by default)
 * const room = await joinLiveKitRoom('my-room', 'Alice', 'your-auth-token');
 * 
 * // Publish camera/mic (requires canPublish permission)
 * try {
 *   await publishMediaTracks(room);
 * } catch (error) {
 *   console.error('Publishing requires a paid subscription');
 * }
 * 
 * // Clean up on page unload
 * window.addEventListener('beforeunload', () => {
 *   room.disconnect();
 * });
 */

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    fetchLiveKitToken,
    joinLiveKitRoom,
    publishMediaTracks,
  };
}
