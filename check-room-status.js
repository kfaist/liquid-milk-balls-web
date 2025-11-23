// Check LiveKit room status using server SDK
const { RoomServiceClient } = require('livekit-server-sdk');
require('dotenv').config();

const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const INPUT_ROOM = process.env.LIVEKIT_ROOM_NAME || "claymation-live";

async function checkRoomStatus() {
    console.log("🔍 CHECKING LIVEKIT ROOM STATUS");
    console.log("=".repeat(80));
    
    if (!LIVEKIT_API_KEY || !LIVEKIT_API_SECRET || !LIVEKIT_URL) {
        console.log("❌ LiveKit credentials not configured in .env");
        return;
    }
    
    console.log(`\n📊 Configuration:`);
    console.log(`   Server: ${LIVEKIT_URL}`);
    console.log(`   Room: ${INPUT_ROOM}`);
    
    try {
        const client = new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
        
        // List all rooms
        console.log(`\n🔍 Listing all active rooms...`);
        const rooms = await client.listRooms();
        console.log(`   Found ${rooms.length} active room(s)`);
        
        if (rooms.length === 0) {
            console.log("\n⚠️  NO ACTIVE ROOMS");
            console.log("   This means:");
            console.log("   - No publishers are currently connected");
            console.log("   - No viewers are currently connected");
            console.log("\n📋 To test:");
            console.log("   1. Open: http://localhost:3000/publisher.html");
            console.log("   2. Allow camera and click 'Start Publishing'");
            console.log("   3. The room will become active");
            console.log("   4. Run this test again");
            return;
        }
        
        // Find our input room
        const inputRoom = rooms.find(r => r.name === INPUT_ROOM);
        
        if (!inputRoom) {
            console.log(`\n⚠️  Room '${INPUT_ROOM}' not found in active rooms`);
            console.log("   Active rooms:");
            rooms.forEach(r => {
                console.log(`   - ${r.name} (${r.numParticipants} participants)`);
            });
            return;
        }
        
        console.log(`\n✅ ROOM FOUND: ${INPUT_ROOM}`);
        console.log(`   Participants: ${inputRoom.numParticipants}`);
        console.log(`   Max participants: ${inputRoom.maxParticipants || 'unlimited'}`);
        
        // Convert BigInt to Number for date calculation
        const creationTimestamp = Number(inputRoom.creationTime);
        console.log(`   Created: ${new Date(creationTimestamp * 1000).toLocaleString()}`);
        
        // List participants
        if (inputRoom.numParticipants > 0) {
            console.log(`\n👥 Listing participants...`);
            const participants = await client.listParticipants(INPUT_ROOM);
            console.log(`   Found ${participants.length} participant(s):`);
            
            participants.forEach((p, i) => {
                console.log(`\n   Participant ${i + 1}:`);
                console.log(`     Identity: ${p.identity}`);
                console.log(`     SID: ${p.sid}`);
                
                // Convert BigInt to Number for date calculation
                const joinTimestamp = Number(p.joinedAt);
                console.log(`     Joined: ${new Date(joinTimestamp * 1000).toLocaleTimeString()}`);
                
                console.log(`     State: ${p.state}`);
                console.log(`     Tracks:`);
                
                p.tracks.forEach(track => {
                    console.log(`       - ${track.type}: ${track.name || track.sid}`);
                    console.log(`         Muted: ${track.muted}`);
                });
            });
            
            console.log("\n✅ PUBLISHERS ARE ACTIVE!");
            console.log("   The input pipeline is working!");
            console.log("\n📋 Next steps:");
            console.log("   1. In TouchDesigner textport (Alt+T), run:");
            console.log("      execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/ultimate_td_setup.py')");
            console.log("   2. Check Web Client TOP - you should see video!");
            console.log("   3. If not, click Reload parameter");
            
        } else {
            console.log("\n⚠️  Room exists but no participants");
            console.log("   Start a publisher to see participants");
        }
        
    } catch (error) {
        console.log(`\n❌ Error: ${error.message}`);
        console.log("\nDetails:", error);
    }
    
    console.log("\n" + "=".repeat(80));
}

checkRoomStatus();
