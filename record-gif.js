#!/usr/bin/env node

/**
 * Pudding Keycap Raindrop Recording Helper
 * 
 * Uses Puppeteer to capture PNG frames from the pudding-demo page
 * and prints ffmpeg commands for GIF/WebM/MP4 assembly.
 * 
 * Usage:
 *   npm install puppeteer  # First time only
 *   node record-gif.js [options]
 * 
 * Options:
 *   --url URL              URL to record (default: http://localhost:3000/pudding-demo.html)
 *   --duration SECONDS     Recording duration in seconds (default: 15)
 *   --fps FPS              Frames per second (default: 30)
 *   --output-dir PATH      Output directory for frames (default: ./gif-frames)
 *   --width WIDTH          Browser width (default: 1200)
 *   --height HEIGHT        Browser height (default: 800)
 *   --help                 Show this help message
 */

const fs = require('fs');
const path = require('path');

// Check if puppeteer is installed
let puppeteer;
try {
    puppeteer = require('puppeteer');
} catch (error) {
    console.error('❌ Puppeteer is not installed!');
    console.error('Please install it with: npm install puppeteer');
    process.exit(1);
}

// Parse command line arguments
const args = process.argv.slice(2);
const config = {
    url: 'http://localhost:3000/pudding-demo.html',
    duration: 15,
    fps: 30,
    outputDir: './gif-frames',
    width: 1200,
    height: 800
};

for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
        case '--help':
            console.log(fs.readFileSync(__filename, 'utf8').split('\n').slice(3, 20).join('\n'));
            process.exit(0);
        case '--url':
            config.url = args[++i];
            break;
        case '--duration':
            config.duration = parseInt(args[++i]);
            break;
        case '--fps':
            config.fps = parseInt(args[++i]);
            break;
        case '--output-dir':
            config.outputDir = args[++i];
            break;
        case '--width':
            config.width = parseInt(args[++i]);
            break;
        case '--height':
            config.height = parseInt(args[++i]);
            break;
    }
}

const frameInterval = 1000 / config.fps;
const totalFrames = Math.floor(config.duration * config.fps);

console.log('\n🎬 Pudding Keycap Raindrop Recorder\n');
console.log('Configuration:');
console.log(`  URL:         ${config.url}`);
console.log(`  Duration:    ${config.duration}s`);
console.log(`  FPS:         ${config.fps}`);
console.log(`  Total frames:${totalFrames}`);
console.log(`  Output dir:  ${config.outputDir}`);
console.log(`  Resolution:  ${config.width}x${config.height}`);
console.log('');

// Ensure output directory exists
if (!fs.existsSync(config.outputDir)) {
    fs.mkdirSync(config.outputDir, { recursive: true });
    console.log(`✓ Created output directory: ${config.outputDir}`);
}

async function captureFrames() {
    console.log('\n🚀 Launching browser...');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    });
    
    const page = await browser.newPage();
    await page.setViewport({
        width: config.width,
        height: config.height,
        deviceScaleFactor: 1
    });
    
    console.log(`✓ Browser launched\n`);
    console.log(`📡 Loading ${config.url}...`);
    
    await page.goto(config.url, { waitForLoadState: 'networkidle0' });
    
    console.log(`✓ Page loaded\n`);
    console.log('🎬 Starting demo and recording...');
    
    // Click the "Start Demo" button
    await page.evaluate(() => {
        const startBtn = document.getElementById('startBtn');
        if (startBtn) startBtn.click();
    });
    
    // Give it a moment to start
    await new Promise(resolve => setTimeout(resolve, 100));
    
    let frameCount = 0;
    const startTime = Date.now();
    
    console.log('');
    
    // Capture frames
    for (let i = 0; i < totalFrames; i++) {
        const framePath = path.join(config.outputDir, `frame-${String(i).padStart(5, '0')}.png`);
        
        await page.screenshot({
            path: framePath,
            type: 'png'
        });
        
        frameCount++;
        
        // Progress indicator
        const progress = Math.round((frameCount / totalFrames) * 100);
        const bar = '█'.repeat(Math.floor(progress / 2)) + '░'.repeat(50 - Math.floor(progress / 2));
        process.stdout.write(`\r  [${bar}] ${progress}% (${frameCount}/${totalFrames} frames)`);
        
        // Wait for next frame
        const elapsed = Date.now() - startTime;
        const expectedTime = (i + 1) * frameInterval;
        const waitTime = Math.max(0, expectedTime - elapsed);
        
        if (waitTime > 0) {
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }
    }
    
    console.log('\n\n✓ Recording complete!');
    console.log(`✓ Captured ${frameCount} frames to ${config.outputDir}/\n`);
    
    await browser.close();
}

function printFfmpegCommands() {
    console.log('\n📦 FFmpeg Commands:\n');
    console.log('━'.repeat(70));
    
    // High-quality GIF with palette
    console.log('\n🎨 High-Quality GIF (with palette for better colors):');
    console.log('');
    console.log('# Step 1: Generate palette from frames');
    console.log(`ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame-%05d.png \\`);
    console.log('  -vf "palettegen=max_colors=256:stats_mode=full" \\');
    console.log(`  ${config.outputDir}/palette.png`);
    console.log('');
    console.log('# Step 2: Create GIF using palette');
    console.log(`ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame-%05d.png \\`);
    console.log(`  -i ${config.outputDir}/palette.png \\`);
    console.log('  -lavfi "paletteuse=dither=bayer:bayer_scale=5" \\');
    console.log('  pudding-raindrops.gif');
    
    console.log('\n━'.repeat(70));
    
    // WebM (good for web, transparent background support)
    console.log('\n🌐 WebM (great for web, smaller file size):');
    console.log('');
    console.log(`ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame-%05d.png \\`);
    console.log('  -c:v libvpx-vp9 -pix_fmt yuva420p \\');
    console.log('  -b:v 2M -crf 30 \\');
    console.log('  pudding-raindrops.webm');
    
    console.log('\n━'.repeat(70));
    
    // MP4 (best compatibility)
    console.log('\n🎥 MP4 (best compatibility):');
    console.log('');
    console.log(`ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame-%05d.png \\`);
    console.log('  -c:v libx264 -pix_fmt yuv420p \\');
    console.log('  -crf 23 -preset medium \\');
    console.log('  pudding-raindrops.mp4');
    
    console.log('\n━'.repeat(70));
    
    // Optimized small GIF
    console.log('\n📦 Small GIF (optimized for sharing, lower quality):');
    console.log('');
    console.log(`ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame-%05d.png \\`);
    console.log('  -vf "fps=15,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" \\');
    console.log('  pudding-raindrops-small.gif');
    
    console.log('\n━'.repeat(70));
    console.log('\n💡 Tips:');
    console.log('  • Use WebM for best quality-to-size ratio on web');
    console.log('  • Use GIF with palette for social media sharing');
    console.log('  • Use MP4 for maximum compatibility');
    console.log('  • Adjust -crf value (0-51) for quality: lower = better');
    console.log('  • Add -vf scale=WIDTH:-1 to resize output');
    console.log('\n');
}

// Main execution
(async () => {
    try {
        await captureFrames();
        printFfmpegCommands();
        console.log('✨ Done! Use the commands above to create your video/GIF.\n');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
})();
