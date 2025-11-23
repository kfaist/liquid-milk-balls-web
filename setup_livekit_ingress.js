// Create or get LiveKit WHIP Ingress for OBS
const { IngressClient, IngressInput } = require('livekit-server-sdk');
require('dotenv').config();

const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;
const ROOM_NAME = 'processed-output';

console.log('='*70);
console.log('SETTING UP LIVEKIT WHIP INGRESS FOR OBS');
console.log('='*70);

const ingressClient = new IngressClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

async function setupIngress() {
    try {
        // List existing ingress
        console.log('\n[1/3] Checking existing ingress...');
        const ingresses = await ingressClient.listIngress({ roomName: ROOM_NAME });
        
        if (ingresses && ingresses.length > 0) {
            console.log(`[OK] Found ${ingresses.length} existing ingress(es)`);
            
            for (const ingress of ingresses) {
                console.log(`\n[INGRESS] ${ingress.name}`);
                console.log(`  ID: ${ingress.ingressId}`);
                console.log(`  URL: ${ingress.url}`);
                console.log(`  Stream Key: ${ingress.streamKey}`);
                
                // Update OBS config with this ingress
                const fs = require('fs');
                const obsConfig = {
                    type: "whip_custom",
                    settings: {
                        server: ingress.url,
                        bearer_token: ingress.streamKey,
                        use_auth: false,
                        bwtest: false,
                        service: "WHIP"
                    }
                };
                
                const configPath = 'C:\\Users\\krista-showputer\\AppData\\Roaming\\obs-studio\\basic\\profiles\\Untitled\\service.json';
                fs.writeFileSync(configPath, JSON.stringify(obsConfig));
                
                console.log(`\n[SUCCESS] Updated OBS config`);
                console.log(`[FILE] ${configPath}`);
                return;
            }
        } else {
            // Create new ingress
            console.log('[INFO] No existing ingress found');
            console.log('\n[2/3] Creating new WHIP ingress...');
            
            const newIngress = await ingressClient.createIngress({
                inputType: IngressInput.WHIP_INPUT,
                name: `obs-${ROOM_NAME}`,
                roomName: ROOM_NAME,
                participantIdentity: `obs-whip-${Date.now()}`,
                participantName: 'OBS Studio'
            });
            
            console.log(`[CREATED] New ingress`);
            console.log(`  URL: ${newIngress.url}`);
            console.log(`  Stream Key: ${newIngress.streamKey}`);
            
            // Update OBS config
            const fs = require('fs');
            const obsConfig = {
                type: "whip_custom",
                settings: {
                    server: newIngress.url,
                    bearer_token: newIngress.streamKey,
                    use_auth: false,
                    bwtest: false,
                    service: "WHIP"
                }
            };
            
            const configPath = 'C:\\Users\\krista-showputer\\AppData\\Roaming\\obs-studio\\basic\\profiles\\Untitled\\service.json';
            fs.writeFileSync(configPath, JSON.stringify(obsConfig));
            
            console.log(`\n[SUCCESS] Created and configured OBS`);
        }
        
        console.log('\n[3/3] READY TO STREAM');
        console.log('='*70);
        console.log('Next: Restart OBS and click Start Streaming');
        console.log('='*70);
        
    } catch (error) {
        console.error('[ERROR]', error.message);
        console.error('Full error:', error);
    }
}

setupIngress();
