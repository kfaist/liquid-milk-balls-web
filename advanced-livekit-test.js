// ADVANCED LIVEKIT CONNECTION TEST
// This will actually connect to LiveKit and check for publishers

const { Room } = require('livekit-client');
const fetch = require('node-fetch');

async function testLiveKitConnection() {
    console.log("🔍 ADVANCED LIVEKIT CONNECTION TEST");
    console.log("=".repeat(80));
    
    let room = null;
    
    try {
        // Get viewer token
        console.log("\n1️⃣ Getting viewer token...");
        const response = await fetch('http://localhost:3000/api/viewer-token');
        const data = await response.json();
        console.log(`  ✅ Token received for room: ${data.room}`);
        console.log(`     Server: ${data.url}`);
        
        // Create room
        console.log("\n2️⃣ Creating LiveKit room...");
        room = new Room({
            adaptiveStream: true,
            dynacast: true,
        });
        
        // Set up event handlers
        room.on('connected', () => {
            console.log("  ✅ Connected to LiveKit room!");
        });
        
        room.on('participantConnected', (participant) => {
            console.log(`  👤 Participant connected: ${participant.identity}`);
        });
        
        room.on('trackSubscribed', (track, publication, participant) => {
            console.log(`  📹 ${track.kind} track from ${participant.identity}`);
        });
        
        // Connect
        console.log("\n3️⃣ Connecting to LiveKit...");
        await room.connect(data.url, data.token);
        console.log("  ✅ Successfully connected!");
        
        // Wait a moment for any existing publishers to be discovered
        console.log("\n4️⃣ Checking for publishers...");
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const participants = Array.from(room.remoteParticipants.values());
        console.log(`  Found ${participants.length} remote participant(s)`);
        
        if (participants.length > 0) {
            console.log("\n📊 ACTIVE PUBLISHERS:");
            participants.forEach((p, i) => {
                console.log(`\n  Publisher ${i + 1}:`);
                console.log(`    Identity: ${p.identity}`);
                console.log(`    SID: ${p.sid}`);
                
                const videoTracks = Array.from(p.videoTrackPublications.values());
                const audioTracks = Array.from(p.audioTrackPublications.values());
                
                console.log(`    Video tracks: ${videoTracks.length}`);
                console.log(`    Audio tracks: ${audioTracks.length}`);
                
                videoTracks.forEach(track => {
                    console.log(`      - Video: ${track.trackSid} (${track.isSubscribed ? 'subscribed' : 'not subscribed'})`);
                });
                
                audioTracks.forEach(track => {
                    console.log(`      - Audio: ${track.trackSid} (${track.isSubscribed ? 'subscribed' : 'not subscribed'})`);
                });
            });
            
            console.log("\n✅ PUBLISHERS DETECTED!");
            console.log("   This means the input pipeline is working!");
            console.log("   If you don't see video in TouchDesigner:");
            console.log("   1. Check Web Client TOP URL is correct");
            console.log("   2. Click Reload parameter on Web Client TOP");
            console.log("   3. Check browser console for errors");
            
        } else {
            console.log("\n⚠️  NO PUBLISHERS FOUND");
            console.log("   To test the full pipeline:");
            console.log("   1. Open: http://localhost:3000/publisher.html");
            console.log("   2. Allow camera access");
            console.log("   3. Click 'Start Publishing'");
            console.log("   4. Run this test again");
        }
        
        // Disconnect
        console.log("\n5️⃣ Disconnecting...");
        await room.disconnect();
        console.log("  ✅ Disconnected cleanly");
        
        console.log("\n" + "=".repeat(80));
        console.log("✅ CONNECTION TEST COMPLETE");
        console.log("=".repeat(80));
        
        return participants.length > 0;
        
    } catch (error) {
        console.log(`\n❌ ERROR: ${error.message}`);
        console.log("\nStack trace:");
        console.log(error.stack);
        
        if (room) {
            try {
                await room.disconnect();
            } catch (e) {
                // Ignore disconnect errors
            }
        }
        
        return false;
    }
}

// Run the test
testLiveKitConnection()
    .then(hasPublishers => {
        if (hasPublishers) {
            console.log("\n🎉 SUCCESS! Publishers are connected and streaming!");
            process.exit(0);
        } else {
            console.log("\n⚠️  No publishers detected. Start a publisher to test the full pipeline.");
            process.exit(0);
        }
    })
    .catch(error => {
        console.error("\n❌ Test failed:", error);
        process.exit(1);
    });
