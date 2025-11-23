async function testPipeline() {
    console.log("🔍 TESTING LIQUID MILK BALLS INPUT PIPELINE");
    console.log("=" .repeat(80));
    
    const tests = [];
    
    // Test 1: Server is running
    console.log("\n1️⃣ Testing local server...");
    try {
        const response = await fetch('http://localhost:3000/healthz');
        if (response.ok) {
            console.log("  ✅ Server is responding");
            tests.push({name: "Server", status: "PASS"});
        } else {
            throw new Error(`Status: ${response.status}`);
        }
    } catch (error) {
        console.log("  ❌ Server not responding:", error.message);
        tests.push({name: "Server", status: "FAIL", error: error.message});
    }
    
    // Test 2: Publisher token generation
    console.log("\n2️⃣ Testing publisher token generation...");
    try {
        const response = await fetch('http://localhost:3000/api/publisher-token');
        const data = await response.json();
        console.log("  ✅ Publisher token generated");
        console.log("     Room:", data.room);
        console.log("     URL:", data.url);
        tests.push({name: "Publisher Token", status: "PASS"});
    } catch (error) {
        console.log("  ❌ Publisher token failed:", error.message);
        tests.push({name: "Publisher Token", status: "FAIL", error: error.message});
    }
    
    // Test 3: Viewer token generation
    console.log("\n3️⃣ Testing viewer token generation...");
    try {
        const response = await fetch('http://localhost:3000/api/viewer-token');
        const data = await response.json();
        console.log("  ✅ Viewer token generated");
        console.log("     Room:", data.room);
        console.log("     URL:", data.url);
        tests.push({name: "Viewer Token", status: "PASS"});
    } catch (error) {
        console.log("  ❌ Viewer token failed:", error.message);
        tests.push({name: "Viewer Token", status: "FAIL", error: error.message});
    }
    
    // Test 4: HTML files exist
    console.log("\n4️⃣ Testing HTML files...");
    const htmlFiles = ['publisher.html', 'td-input-viewer.html', 'return-viewer.html'];
    let htmlOk = true;
    for (const file of htmlFiles) {
        try {
            const response = await fetch(`http://localhost:3000/${file}`);
            if (response.ok) {
                console.log(`  ✅ ${file} exists`);
            } else {
                console.log(`  ❌ ${file} not found (${response.status})`);
                htmlOk = false;
            }
        } catch (error) {
            console.log(`  ❌ ${file} error:`, error.message);
            htmlOk = false;
        }
    }
    tests.push({name: "HTML Files", status: htmlOk ? "PASS" : "FAIL"});
    
    // Summary
    console.log("\n" + "=".repeat(80));
    console.log("📊 TEST SUMMARY");
    console.log("=".repeat(80));
    
    const passed = tests.filter(t => t.status === "PASS").length;
    const failed = tests.filter(t => t.status === "FAIL").length;
    
    tests.forEach(test => {
        const icon = test.status === "PASS" ? "✅" : "❌";
        console.log(`${icon} ${test.name}: ${test.status}`);
        if (test.error) {
            console.log(`   Error: ${test.error}`);
        }
    });
    
    console.log(`\n📈 Results: ${passed} passed, ${failed} failed`);
    
    if (failed === 0) {
        console.log("\n🎉 ALL TESTS PASSED! Pipeline is ready!");
        console.log("\n📋 NEXT STEPS:");
        console.log("   1. Open http://localhost:3000/publisher.html in Firefox");
        console.log("      - Allow camera access when prompted");
        console.log("      - Click 'Start Publishing'");
        console.log("   2. In TouchDesigner textport (Alt+T), run:");
        console.log("      execfile('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/auto_config_webclient.py')");
        console.log("   3. Look at the Web Client TOP - you should see video!");
    } else {
        console.log("\n⚠️ Some tests failed. Fix the issues above before proceeding.");
    }
}

testPipeline().catch(console.error);
