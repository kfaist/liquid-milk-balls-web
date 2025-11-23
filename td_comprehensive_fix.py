# COMPREHENSIVE TOUCHDESIGNER VIDEO FIX
# This script tries multiple approaches to get camera video working

import time

print("=" * 70)
print("TOUCHDESIGNER WEBRENDER VIDEO FIX - COMPREHENSIVE APPROACH")
print("=" * 70)

# Approach 1: Force video with diagnostic info
print("\n[APPROACH 1] Loading diagnostic video page...")
wr1 = op('/project1/webrender1')
wr1.par.url = 'http://localhost:3000/force_video.html'
wr1.par.reloadsrc.pulse()
print("✓ Loaded force_video.html")
print("  Wait 3 seconds for page to load...")
time.sleep(3)

# Check TOP output
print("\n[CHECKING] WebRender TOP output status:")
print(f"  Width: {wr1.width}")
print(f"  Height: {wr1.height}")
print(f"  Active: {wr1.par.active.eval()}")
print(f"  Cook Always: {wr1.par.alwayscook.eval()}")

# Approach 2: Try Canvas-based capture
print("\n[APPROACH 2] Creating Canvas-based capture page...")
canvas_html = """<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>Canvas Video Capture</title>
<style>
body { margin: 0; background: #000; }
#canvas { width: 100vw; height: 100vh; display: block; }
#info { position: fixed; top: 10px; left: 10px; background: lime; color: black; padding: 10px; font-family: monospace; font-size: 12px; z-index: 1000; }
</style>
</head>
<body>
<canvas id="canvas" width="1280" height="720"></canvas>
<div id="info">Starting...</div>
<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const info = document.getElementById('info');
const video = document.createElement('video');
video.autoplay = true;
video.playsInline = true;
video.muted = true;

navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
  .then(stream => {
    video.srcObject = stream;
    info.innerHTML = 'STREAM OK - Drawing to canvas...';
    
    function drawFrame() {
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        info.innerHTML = 'RENDERING<br>Video: ' + video.videoWidth + 'x' + video.videoHeight + '<br>Canvas: ' + canvas.width + 'x' + canvas.height + '<br>Frame: ' + Date.now();
      }
      requestAnimationFrame(drawFrame);
    }
    
    video.addEventListener('loadedmetadata', () => {
      info.innerHTML = 'Video loaded! Starting render...';
      drawFrame();
    });
  })
  .catch(err => {
    info.innerHTML = 'ERROR: ' + err.message;
    info.style.background = 'red';
    info.style.color = 'white';
  });
</script>
</body>
</html>"""

# Write canvas test file
import os
canvas_path = r"C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\canvas_video_test.html"
with open(canvas_path, 'w', encoding='utf-8') as f:
    f.write(canvas_html)
print(f"✓ Created {canvas_path}")

# Load canvas test
print("\n[LOADING] Canvas video test...")
wr1.par.url = 'http://localhost:3000/canvas_video_test.html'
wr1.par.reloadsrc.pulse()
print("✓ Loaded canvas_video_test.html")
print("  Wait 3 seconds for canvas render...")
time.sleep(3)

# Check if canvas is rendering
print("\n[CHECKING] Canvas test results:")
print(f"  TOP Width: {wr1.width}")
print(f"  TOP Height: {wr1.height}")

# Approach 3: Try both WebRender TOPs with canvas
print("\n[APPROACH 3] Setting up BOTH WebRender TOPs with canvas...")
wr2 = op('/project1/webrender_livekit_input')
wr2.par.url = 'http://localhost:3000/canvas_video_test.html'
wr2.par.reloadsrc.pulse()
print("✓ Both TOPs now using canvas test")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE - CHECK RESULTS:")
print("=" * 70)
print("\n1. Look at /project1/webrender1 output")
print("2. Look at /project1/webrender_livekit_input output")
print("3. Check if you see:")
print("   - Green info box with 'RENDERING' message")
print("   - Actual video frames")
print("\nIf you see the info box but NO video:")
print("   -> CEF may not support video elements")
print("   -> Canvas approach should work")
print("\nIf you see NOTHING:")
print("   -> Check Dialogs → Console for errors")
print("   -> May need to restart TouchDesigner")
print("\n" + "=" * 70)
