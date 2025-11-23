(0)// record-gif.js
(0)// Usage example:
(0)//   npm install puppeteer
(0)//   node record-gif.js --url=http://localhost:3000/pudding-demo.html --out=pudding.gif --duration=6 --fps=18 --width=900
(0)//
(0)// Captures PNG frames with Puppeteer and then you assemble into a gif with ffmpeg (commands printed).
(0)const fs = require('fs');
(0)const path = require('path');
(0)const puppeteer = require('puppeteer');
(0)
(0)function parseArgs() {
(0)  const args = {};
(0)  process.argv.slice(2).forEach(arg => {
(0)    const m = arg.match(/^--([^=]+)=?(.*)$/);
(0)    if (m) args[m[1]] = m[2] || true;
(0)  });
(0)  return args;
(0)}
(0)
(0)(async () => {
(0)  const args = parseArgs();
(0)  const url = args.url || 'http://localhost:3000/pudding-demo.html';
(0)  const outDir = args.framesDir || path.join(process.cwd(), 'gif-frames');
(0)  const duration = parseFloat(args.duration || 6) * 1000; // ms
(0)  const fps = parseInt(args.fps || 18, 10);
(0)  const width = parseInt(args.width || 900, 10);
(0)
(0)  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
(0)
(0)  console.log(`Opening ${url}`);
(0)  const browser = await puppeteer.launch({
(0)    defaultViewport: { width: width, height: Math.round(width * 420/900) },
(0)    args: ['--no-sandbox', '--disable-setuid-sandbox']
(0)  });
(0)  const page = await browser.newPage();
(0)  await page.setViewport({ width: width, height: Math.round(width * 420/900) });
(0)
(0)  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
(0)  console.log('Page loaded. Starting capture sequence...');
(0)
(0)  // Ensure the demo helper exists or create a fallback that clicks Start Demo button
(0)  const startResult = await page.evaluate(() => {
(0)    if (window.startWatermarkTimer) { window.startWatermarkTimer(); return 'startWatermarkTimer()'; }
(0)    const btn = document.querySelector('#startBtn') || document.querySelector('button');
(0)    if (btn) { btn.click(); return 'clicked button'; }
(0)    return 'no-start-action';
(0)  });
(0)  console.log('Trigger action result:', startResult);
(0)
(0)  // small warm-up wait
(0)  await page.waitForTimeout(350);
(0)
(0)  const totalFrames = Math.ceil((duration / 1000) * fps);
(0)  const intervalMs = 1000 / fps;
(0)
(0)  console.log(`Capturing ${totalFrames} frames at ${fps} fps (~${duration/1000}s). Frames in: ${outDir}`);
(0)
(0)  for (let i = 0; i < totalFrames; i++) {
(0)    const name = path.join(outDir, `frame_${String(i).padStart(4,'0')}.png`);
(0)    await page.screenshot({ path: name, omitBackground: true });
(0)    if (i % Math.ceil(fps/2) === 0) process.stdout.write('.');
(0)    await page.waitForTimeout(intervalMs);
(0)  }
(0)  process.stdout.write('\n');
(0)
(0)  console.log('Capture finished. Closing browser.');
(0)  await browser.close();
(0)
(0)  console.log('');
(0)  console.log('Now run the ffmpeg commands below to assemble a high-quality GIF/WebM/MP4:');
(0)  console.log('');
(0)  console.log(`# generate palette (better colors)`);
(0)  console.log(`ffmpeg -y -framerate ${fps} -i ${outDir}/frame_%04d.png -vf "scale=${width}:-1:flags=lanczos,palettegen" palette.png`);
(0)  console.log('');
(0)  console.log(`# render GIF using the palette (tweak -r to control output fps)`);
(0)  console.log(`ffmpeg -y -framerate ${fps} -i ${outDir}/frame_%04d.png -i palette.png -lavfi "scale=${width}:-1:flags=lanczos [x]; [x][1:v] paletteuse" ${args.out || 'pudding.gif'}`);
(0)  console.log('');
(0)  console.log('# Optional: create WebM and MP4');
(0)  console.log(`ffmpeg -y -framerate ${fps} -i ${outDir}/frame_%04d.png -c:v libvpx-vp9 -b:v 0 -crf 30 pudding.webm`);
(0)  console.log(`ffmpeg -y -framerate ${fps} -i ${outDir}/frame_%04d.png -c:v libx264 -crf 23 -preset medium pudding.mp4`);
(0)})();
