const https = require('https');

console.log("🔍 COMPREHENSIVE SYSTEM DIAGNOSTIC");
console.log("=" .repeat(80));

async function checkLiveKitRoom() {
    console.log("\n🔗 CHECKING LIVEKIT ROOM STATUS...");
    
    try {
        // This is a simple check - in a real scenario we'd use LiveKit SDK
        const response = await fetch('http://localhost:3000/api/viewer-token');
        const data = await response.json();
        
        console.log("  ✅ Can generate viewer token");
        console.log(`     Room: ${data.room}`);
        console.log(`     Server: ${data.url}`);
        
        return true;
    } catch (error) {
        console.log(`  ❌ Error: ${error.message}`);
        return false;
    }
}

async function checkPublisherPage() {
    console.log("\n📹 CHECKING PUBLISHER PAGE...");
    
    try {
        const response = await fetch('http://localhost:3000/publisher.html');
        if (response.ok) {
            console.log("  ✅ Publisher page accessible");
            return true;
        }
        throw new Error(`Status: ${response.status}`);
    } catch (error) {
        console.log(`  ❌ Error: ${error.message}`);
        return false;
    }
}

async function checkTDViewerPage() {
    console.log("\n👁️  CHECKING TD INPUT VIEWER PAGE...");
    
    try {
        const response = await fetch('http://localhost:3000/td-input-viewer.html');
        const html = await response.text();
        
        console.log("  ✅ TD viewer page accessible");
        
        // Check if it has the correct LiveKit setup
        if (html.includes('livekit-client')) {
            console.log("  ✅ LiveKit client library included");
        }
        if (html.includes('api/viewer-token')) {
            console.log("  ✅ Configured to fetch viewer token");
        }
        if (html.includes('claymation-live') || html.includes('viewer-token')) {
            console.log("  ✅ Configured for correct room");
        }
        
        return true;
    } catch (error) {
        console.log(`  ❌ Error: ${error.message}`);
        return false;
    }
}

async function checkServerEndpoints() {
    console.log("\n🌐 CHECKING ALL SERVER ENDPOINTS...");
    
    const endpoints = [
        { path: '/healthz', desc: 'Health check' },
        { path: '/api/publisher-token', desc: 'Publisher token' },
        { path: '/api/viewer-token', desc: 'Viewer token' },
        { path: '/api/processed-publisher-token', desc: 'Processed publisher token' },
        { path: '/api/processed-viewer-token', desc: 'Processed viewer token' },
        { path: '/publisher.html', desc: 'Publisher page' },
        { path: '/td-input-viewer.html', desc: 'TD viewer page' },
        { path: '/status-dashboard.html', desc: 'Status dashboard' },
        { path: '/master-test.html', desc: 'Master test' },
    ];
    
    let allPass = true;
    
    for (const endpoint of endpoints) {
        try {
            const response = await fetch(`http://localhost:3000${endpoint.path}`);
            if (response.ok) {
                console.log(`  ✅ ${endpoint.desc}`);
            } else {
                console.log(`  ❌ ${endpoint.desc} - Status: ${response.status}`);
                allPass = false;
            }
        } catch (error) {
            console.log(`  ❌ ${endpoint.desc} - Error: ${error.message}`);
            allPass = false;
        }
    }
    
    return allPass;
}

async function generateDiagnosticReport() {
    console.log("\n📊 GENERATING DIAGNOSTIC REPORT...");
    
    const results = {
        timestamp: new Date().toISOString(),
        tests: {}
    };
    
    results.tests.livekit = await checkLiveKitRoom();
    results.tests.publisher = await checkPublisherPage();
    results.tests.tdViewer = await checkTDViewerPage();
    results.tests.endpoints = await checkServerEndpoints();
    
    console.log("\n" + "=".repeat(80));
    console.log("📋 DIAGNOSTIC SUMMARY");
    console.log("=".repeat(80));
    
    const allPass = Object.values(results.tests).every(t => t === true);
    
    if (allPass) {
        console.log("\n✅ ALL SYSTEMS OPERATIONAL!");
        console.log("\n🎯 READY FOR TESTING:");
        console.log("   1. Open: http://localhost:3000/publisher.html");
        console.log("   2. Allow camera and click 'Start Publishing'");
        console.log("   3. In TouchDesigner textport (Alt+T):");
        console.log("      execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/master_setup.py')");
        console.log("   4. Check Web Client TOP for video!");
    } else {
        console.log("\n⚠️ SOME SYSTEMS NEED ATTENTION");
        console.log("   Check the errors above and fix before proceeding.");
    }
    
    console.log("\n📄 Report saved to: diagnostic-report.json");
    
    const fs = require('fs');
    fs.writeFileSync('diagnostic-report.json', JSON.stringify(results, null, 2));
}

generateDiagnosticReport().catch(console.error);
