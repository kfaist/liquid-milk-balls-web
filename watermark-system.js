// Progressive Watermark System
// Starts at 7 minutes, gradually increases to full watermark at 10 minutes

(function() {
    'use strict';

    // Timing configuration (in milliseconds)
    const PHASE_START = 7 * 60 * 1000;  // 7 minutes
    const PHASE_1 = 8 * 60 * 1000;      // 8 minutes
    const PHASE_2 = 9 * 60 * 1000;      // 9 minutes
    const PHASE_3 = 10 * 60 * 1000;     // 10 minutes

    let startTime = null;
    let watermarkIntervalId = null;
    let textOverlayVisible = false;

    // Initialize watermark system when remote video starts playing
    function initWatermark() {
        const remoteVideo = document.getElementById('remoteVideo');
        const fullscreenVideo = document.getElementById('fullscreenVideo');

        if (!remoteVideo) return;

        // Start timer when remote video begins playing
        remoteVideo.addEventListener('playing', () => {
            if (!startTime) {
                console.log('Watermark timer started');
                startTime = Date.now();
                startWatermarkLoop();
            }
        });

        // Also handle fullscreen video
        if (fullscreenVideo) {
            fullscreenVideo.addEventListener('playing', () => {
                if (!startTime) {
                    console.log('Watermark timer started (fullscreen)');
                    startTime = Date.now();
                    startWatermarkLoop();
                }
            });
        }
    }

    // Main watermark loop
    function startWatermarkLoop() {
        if (watermarkIntervalId) return; // Already running

        watermarkIntervalId = setInterval(() => {
            const elapsed = Date.now() - startTime;
            updateWatermark(elapsed);
        }, 1000); // Check every second
    }

    // Update watermark based on elapsed time
    function updateWatermark(elapsed) {
        if (elapsed < PHASE_START) {
            // 0-7 minutes: No watermark
            return;
        }

        const remoteVideo = document.getElementById('remoteVideo');
        const fullscreenVideo = document.getElementById('fullscreenVideo');

        // Determine current phase and get raindrop frequency
        let frequency = getDropFrequency(elapsed);

        // Create raindrop on both video elements
        if (Math.random() < frequency) {
            if (remoteVideo && remoteVideo.srcObject) {
                createRaindrop(remoteVideo.parentElement);
            }
            if (fullscreenVideo && fullscreenVideo.srcObject) {
                createRaindrop(fullscreenVideo.parentElement);
            }
        }

        // Show text overlay at 10+ minutes
        if (elapsed >= PHASE_3 && !textOverlayVisible) {
            showTextOverlay();
            textOverlayVisible = true;
        }
    }

    // Get raindrop frequency based on elapsed time
    function getDropFrequency(elapsed) {
        if (elapsed < PHASE_START) {
            return 0; // No watermark
        } else if (elapsed < PHASE_1) {
            // 7-8 min: Option 1 - Subtle (every 8-10 seconds)
            return 0.01; // ~1% chance per second = ~every 10 seconds
        } else if (elapsed < PHASE_2) {
            // 8-9 min: Increasing (every 5-7 seconds)
            return 0.02; // ~2% chance per second = ~every 5 seconds
        } else if (elapsed < PHASE_3) {
            // 9-10 min: More prominent (every 2-4 seconds)
            return 0.04; // ~4% chance per second = ~every 2.5 seconds
        } else {
            // 10+ min: Option 3 - Cannot be ignored (every 1-2 seconds)
            return 0.08; // ~8% chance per second = ~every 1.25 seconds
        }
    }

    // Create a raindrop ripple effect
    function createRaindrop(container) {
        const raindrop = document.createElement('div');
        raindrop.className = 'video-raindrop';

        // Random position within the video
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        raindrop.style.left = x + '%';
        raindrop.style.top = y + '%';

        // Random size and duration based on phase
        const elapsed = Date.now() - startTime;
        let size, duration, intensity;

        if (elapsed < PHASE_1) {
            // Subtle
            size = 40 + Math.random() * 40; // 40-80px
            duration = 2.5 + Math.random() * 1.5; // 2.5-4s
            intensity = 0.15;
        } else if (elapsed < PHASE_2) {
            // Medium
            size = 60 + Math.random() * 60; // 60-120px
            duration = 2 + Math.random() * 1; // 2-3s
            intensity = 0.25;
        } else if (elapsed < PHASE_3) {
            // Prominent
            size = 80 + Math.random() * 80; // 80-160px
            duration = 1.5 + Math.random() * 1; // 1.5-2.5s
            intensity = 0.35;
        } else {
            // Cannot be ignored
            size = 100 + Math.random() * 100; // 100-200px
            duration = 1 + Math.random() * 1; // 1-2s
            intensity = 0.45;
        }

        raindrop.style.width = size + 'px';
        raindrop.style.height = size + 'px';
        raindrop.style.animationDuration = duration + 's';
        raindrop.style.setProperty('--raindrop-intensity', intensity);

        container.appendChild(raindrop);

        // Remove after animation
        setTimeout(() => {
            raindrop.remove();
        }, duration * 1000);
    }

    // Show glassmorphism text overlay at 10 minutes
    function showTextOverlay() {
        const remoteWrapper = document.getElementById('remoteVideo')?.parentElement;
        const fullscreenVideo = document.getElementById('fullscreenVideo')?.parentElement;

        // Create overlay for remote video
        if (remoteWrapper && !remoteWrapper.querySelector('.watermark-text-overlay')) {
            const overlay = createTextOverlay();
            remoteWrapper.appendChild(overlay);
        }

        // Create overlay for fullscreen video
        if (fullscreenVideo && !fullscreenVideo.querySelector('.watermark-text-overlay')) {
            const overlay = createTextOverlay();
            fullscreenVideo.appendChild(overlay);
        }
    }

    // Create glassmorphism text overlay element
    function createTextOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'watermark-text-overlay';

        const textContainer = document.createElement('div');
        textContainer.className = 'watermark-glass-panel';

        const title = document.createElement('div');
        title.className = 'watermark-title';
        title.textContent = "The Mirror's Echo";

        const subtitle = document.createElement('div');
        subtitle.className = 'watermark-subtitle';
        subtitle.textContent = 'Demo Version';

        const licensing = document.createElement('div');
        licensing.className = 'watermark-licensing';
        licensing.innerHTML = 'Commercial licensing available<br>Contact for custom quote';

        textContainer.appendChild(title);
        textContainer.appendChild(subtitle);
        textContainer.appendChild(licensing);
        overlay.appendChild(textContainer);

        return overlay;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWatermark);
    } else {
        initWatermark();
    }
})();
