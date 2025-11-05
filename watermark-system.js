// Progressive Watermark System
// Starts at 7 minutes, gradually increases to full watermark at 10 minutes

(function() {
    'use strict';

    // Timing configuration (in milliseconds)
    const PHASE_START = 8 * 60 * 1000;  // 8 minutes - watermark begins (loss of control)
    const PHASE_1 = 9 * 60 * 1000;      // 9 minutes
    const PHASE_2 = 10 * 60 * 1000;     // 10 minutes
    const PHASE_3 = 11 * 60 * 1000;     // 11 minutes

    let startTime = null;
    let watermarkIntervalId = null;
    let textOverlayVisible = false;
    let raindropCount = 0; // Track raindrops for color changes

    // Manual start function (exposed globally for testing)
    function startWatermarkTimer() {
        if (!startTime) {
            console.log('Watermark timer started manually');
            startTime = Date.now();
            startWatermarkLoop();
        }
    }

    // Initialize watermark system when remote video starts playing
    function initWatermark() {
        const remoteVideo = document.getElementById('remoteVideo');
        const fullscreenVideo = document.getElementById('fullscreenVideo');

        // Expose manual start function globally for testing
        window.startWatermarkTimer = startWatermarkTimer;

        if (!remoteVideo) return;

        // Start timer when remote video begins playing
        remoteVideo.addEventListener('playing', () => {
            if (!startTime) {
                console.log('Watermark timer started (video playing)');
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

        // TEMPORARY: Auto-start timer on page load for testing (remove in production)
        // Uncomment the line below to auto-start the 8-minute countdown
        // setTimeout(startWatermarkTimer, 1000);
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
        // Update body class for site-wide effects
        updateSitePhase(elapsed);

        if (elapsed < PHASE_START) {
            // 0-8 minutes: No automatic watermark (playful click interaction only)
            return;
        }

        // At 8+ minutes: Create raindrops on the overlay (OVER everything, not capturable)
        const watermarkOverlay = document.getElementById('watermark-overlay');

        // Determine current phase and get raindrop frequency
        let frequency = getDropFrequency(elapsed);

        // Create raindrop on the overlay (appears over entire page)
        if (watermarkOverlay && Math.random() < frequency) {
            createRaindrop(watermarkOverlay);
        }

        // Show text overlay at 10+ minutes
        if (elapsed >= PHASE_3 && !textOverlayVisible) {
            showTextOverlay();
            textOverlayVisible = true;
        }
    }

    // Update site-wide shimmer phase based on elapsed time
    function updateSitePhase(elapsed) {
        const body = document.body;

        // Remove all phase classes
        body.classList.remove('temporal-phase-1', 'temporal-phase-2', 'temporal-phase-3', 'temporal-phase-4');

        // Add appropriate phase class
        if (elapsed >= PHASE_3) {
            body.classList.add('temporal-phase-4'); // 10+ min: Undeniable
        } else if (elapsed >= PHASE_2) {
            body.classList.add('temporal-phase-3'); // 9-10 min: Presence
        } else if (elapsed >= PHASE_1) {
            body.classList.add('temporal-phase-2'); // 8-9 min: Murmur
        } else if (elapsed >= PHASE_START) {
            body.classList.add('temporal-phase-1'); // 7-8 min: Whisper
        }
    }

    // Get raindrop frequency based on elapsed time
    function getDropFrequency(elapsed) {
        if (elapsed < PHASE_START) {
            return 0; // No automatic watermark (0-8 min: playful clicks only)
        } else if (elapsed < PHASE_1) {
            // 8-9 min: Loss of control begins (every 8-12 seconds)
            return 0.01; // ~1% chance per second = ~every 10 seconds
        } else if (elapsed < PHASE_2) {
            // 9-10 min: Increasing presence (every 4-6 seconds)
            return 0.025; // ~2.5% chance per second = ~every 5 seconds
        } else if (elapsed < PHASE_3) {
            // 10-11 min: More prominent (every 2-3 seconds)
            return 0.05; // ~5% chance per second = ~every 2 seconds
        } else {
            // 11+ min: Cannot be ignored (every 0.5-1.5 seconds)
            return 0.12; // ~12% chance per second = ~every 0.8 seconds
        }
    }

    // Get current color hue based on raindrop count (changes every 5 raindrops)
    function getCurrentHue() {
        return (Math.floor(raindropCount / 5) * 30) % 360;
    }

    // Create a raindrop ripple effect
    function createRaindrop(container) {
        raindropCount++; // Increment for color changes

        const raindrop = document.createElement('div');
        raindrop.className = 'video-raindrop';

        // Random position within the video
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        raindrop.style.left = x + '%';
        raindrop.style.top = y + '%';

        // Get current hue for color cycling
        const hue = getCurrentHue();

        // Random size and duration based on phase
        const elapsed = Date.now() - startTime;
        let size, duration, intensity;

        if (elapsed < PHASE_1) {
            // Very subtle hint/preview
            size = 30 + Math.random() * 30; // 30-60px (smaller)
            duration = 3 + Math.random() * 2; // 3-5s (slower fade)
            intensity = 0.08; // Very faint
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
        raindrop.style.setProperty('--raindrop-hue', hue);

        // Add shimmer line effect (like mirror circle)
        const shimmer = document.createElement('div');
        shimmer.className = 'raindrop-shimmer';
        shimmer.style.animationDuration = (duration * 0.5) + 's'; // Faster than raindrop
        shimmer.style.setProperty('--shimmer-hue', hue);
        raindrop.appendChild(shimmer);

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
            // Update colors periodically
            setInterval(() => updateOverlayColors(overlay), 1000);
        }

        // Create overlay for fullscreen video
        if (fullscreenVideo && !fullscreenVideo.querySelector('.watermark-text-overlay')) {
            const overlay = createTextOverlay();
            fullscreenVideo.appendChild(overlay);
            // Update colors periodically
            setInterval(() => updateOverlayColors(overlay), 1000);
        }
    }

    // Update overlay colors based on current hue
    function updateOverlayColors(overlay) {
        const hue = getCurrentHue();
        const panel = overlay.querySelector('.watermark-glass-panel');
        if (panel) {
            panel.style.borderColor = `hsla(${hue}, 70%, 60%, 0.4)`;
            panel.style.boxShadow = `
                0 8px 32px 0 rgba(0, 0, 0, 0.6),
                inset 0 0 20px hsla(${hue}, 70%, 60%, 0.1),
                0 0 40px hsla(${hue}, 70%, 60%, 0.2)
            `;
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
