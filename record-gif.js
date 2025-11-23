#!/usr/bin/env node

/**
 * Pudding Keycap Raindrop Recorder
 * 
 * Uses Puppeteer to load a demo page, trigger the animation,
 * capture PNG frames, and output ffmpeg commands for encoding.
 * 
 * Usage:
 *   npm install puppeteer  # Install if needed
 *   node record-gif.js [url] [duration] [fps]
 * 
 * Examples:
 *   node record-gif.js http://localhost:3000/pudding-demo.html 25 30
 *   node record-gif.js http://localhost:3000/pudding-demo.html 30 24
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Configuration
const DEFAULT_URL = 'http://localhost:3000/pudding-demo.html';
const DEFAULT_DURATION = 25; // seconds
const DEFAULT_FPS = 30;
const OUTPUT_DIR = './frames';

// Parse command line arguments
const args = process.argv.slice(2);
const TARGET_URL = args[0] || DEFAULT_URL;
const DURATION_SECONDS = parseInt(args[1]) || DEFAULT_DURATION;
const FPS = parseInt(args[2]) || DEFAULT_FPS;

const FRAME_INTERVAL = 1000 / FPS; // milliseconds between frames
const TOTAL_FRAMES = DURATION_SECONDS * FPS;

console.log('🎬 Pudding Keycap Recorder');
console.log('━'.repeat(50));
console.log(`URL:      ${TARGET_URL}`);
console.log(`Duration: ${DURATION_SECONDS}s`);
console.log(`FPS:      ${FPS}`);
console.log(`Frames:   ${TOTAL_FRAMES}`);
console.log(`Output:   ${OUTPUT_DIR}/`);
console.log('━'.repeat(50));

async function captureFrames() {
    // Create output directory
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    } else {
        // Clean existing frames
        const files = fs.readdirSync(OUTPUT_DIR);
        files.forEach(file => {
            if (file.endsWith('.png')) {
                fs.unlinkSync(path.join(OUTPUT_DIR, file));
            }
        });
    }

    console.log('\n🚀 Launching browser...');
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-web-security'
        ]
    });

    const page = await browser.newPage();
    await page.setViewport({ 
        width: 1920, 
        height: 1080,
        deviceScaleFactor: 1
    });

    console.log('📄 Loading page...');
    await page.goto(TARGET_URL, { 
        waitUntil: 'networkidle0',
        timeout: 30000
    });

    // Wait for page to be fully loaded
    await page.waitForTimeout(1000);

    console.log('▶️  Starting demo...');
    // Click the start button
    await page.evaluate(() => {
        const startBtn = document.querySelector('button');
        if (startBtn) startBtn.click();
        // Or call startDemo() if available
        if (typeof startDemo === 'function') {
            startDemo();
        }
    });

    console.log('🎥 Capturing frames...');
    const startTime = Date.now();
    let frameCount = 0;

    // Capture frames at regular intervals
    while (frameCount < TOTAL_FRAMES) {
        const targetTime = frameCount * FRAME_INTERVAL;
        const actualTime = Date.now() - startTime;
        
        // Wait if we're ahead of schedule
        if (actualTime < targetTime) {
            await page.waitForTimeout(targetTime - actualTime);
        }

        // Capture frame
        const frameNumber = String(frameCount).padStart(5, '0');
        const filename = path.join(OUTPUT_DIR, `frame_${frameNumber}.png`);
        
        await page.screenshot({
            path: filename,
            type: 'png'
        });

        frameCount++;
        
        // Progress indicator
        if (frameCount % (FPS * 2) === 0 || frameCount === TOTAL_FRAMES) {
            const progress = ((frameCount / TOTAL_FRAMES) * 100).toFixed(1);
            const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
            process.stdout.write(`\r  Frame ${frameCount}/${TOTAL_FRAMES} (${progress}%) - ${elapsed}s elapsed`);
        }
    }

    console.log('\n\n✅ Capture complete!');
    await browser.close();

    // Print encoding commands
    printEncodingCommands();
}

function printEncodingCommands() {
    console.log('\n📦 Encoding Commands:');
    console.log('━'.repeat(50));
    
    console.log('\n🎞️  High-Quality GIF (Optimized):');
    console.log(`ffmpeg -framerate ${FPS} -i ${OUTPUT_DIR}/frame_%05d.png -vf "fps=${FPS},scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 pudding-keycaps.gif`);
    
    console.log('\n🎥 WebM (Best for web):');
    console.log(`ffmpeg -framerate ${FPS} -i ${OUTPUT_DIR}/frame_%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 2M -auto-alt-ref 0 pudding-keycaps.webm`);
    
    console.log('\n🎬 MP4 (Universal):');
    console.log(`ffmpeg -framerate ${FPS} -i ${OUTPUT_DIR}/frame_%05d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p pudding-keycaps.mp4`);
    
    console.log('\n💎 MP4 (Transparent/HEVC - for ProRes compatibility):');
    console.log(`ffmpeg -framerate ${FPS} -i ${OUTPUT_DIR}/frame_%05d.png -c:v libx265 -preset slow -crf 18 -pix_fmt yuva420p -tag:v hvc1 pudding-keycaps-alpha.mp4`);
    
    console.log('\n📏 Smaller GIF (Reduced size):');
    console.log(`ffmpeg -framerate ${FPS} -i ${OUTPUT_DIR}/frame_%05d.png -vf "fps=${Math.floor(FPS/2)},scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0 pudding-keycaps-small.gif`);
    
    console.log('\n━'.repeat(50));
    console.log('\n💡 Tips:');
    console.log('  • Adjust -b:v or -crf for quality vs file size');
    console.log('  • Use scale=XXX:-1 to change output resolution');
    console.log('  • Add -loop 0 to GIFs for infinite loop');
    console.log('  • WebM with alpha: add -pix_fmt yuva420p');
    console.log('  • For social media: consider 600-800px width');
    console.log('\n🎨 Color Matching:');
    console.log('  • Upload a sample photo to match colors');
    console.log('  • Edit CSS variables in pudding-demo.html or styles.css');
    console.log('  • Adjust --raindrop-hue for base color');
    console.log('  • Adjust --raindrop-intensity for brightness');
    console.log('');
}

// Check if puppeteer is installed
async function checkDependencies() {
    try {
        require.resolve('puppeteer');
        return true;
    } catch (e) {
        console.error('❌ Error: Puppeteer is not installed.');
        console.error('\nTo install, run:');
        console.error('  npm install puppeteer');
        console.error('\nOr add to package.json devDependencies:');
        console.error('  "puppeteer": "^21.0.0"');
        return false;
    }
}

// Main execution
(async () => {
    if (!await checkDependencies()) {
        process.exit(1);
    }

    try {
        await captureFrames();
        console.log('✨ All done! Use the commands above to encode your video.\n');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        console.error('\nTroubleshooting:');
        console.error('  • Make sure the target URL is accessible');
        console.error('  • Check that the server is running (npm start)');
        console.error('  • Try a different URL or duration');
        console.error('  • Verify puppeteer installation');
        process.exit(1);
    }
})();
