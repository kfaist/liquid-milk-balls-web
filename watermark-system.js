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

    // Ensure halo styles are present (inject new CSS file if needed)
    function ensureHaloStyles() {
        if (document.querySelector('link[href="/halo-drops.css"], link[href="halo-drops.css"]')) return;
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'halo-drops.css';
        document.head.appendChild(link);
    }

    // Initialize watermark system when remote video starts playing
    function initWatermark() {
        const remoteVideo = document.getElementById('remoteVideo');
        const fullscreenVideo = document.getElementById('fullscreenVideo');

        // Expose manual start function globally for testing
        window.startWatermarkTimer = startWatermarkTimer;

        // Ensure halo stylesheet is available for automatic drops
        ensureHaloStyles();

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
            // Create halo-style drop instead of keycap
            const drop = createRaindrop(elapsed);
            watermarkOverlay.appendChild(drop);
            // remove after its animation (duration + buffer)
            const duration = parseFloat(getComputedStyle(drop).getPropertyValue('--duration')) || 3;
            setTimeout(() => drop.remove(), Math.ceil(duration * 1000) + 800);
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

    // ---- NEW: Create halo-style raindrop element (replaces pudding keycap look) ----
    // This function maps the existing 9-10 minute ramp to glow/halo intensity and spawn depth,
    // rather than to bevel/"bump" variables. It emits per-drop CSS variables used by halo-drops.css.
    function createRaindrop(elapsedMs) {
        raindropCount++;

        // Compute ramp intensity (0..1) across the existing phase window (PHASE_1..PHASE_2)
        const rampStart = PHASE_1;
        const rampEnd = PHASE_2;
        const t = Math.max(0, Math.min(1, (elapsedMs - rampStart) / (rampEnd - rampStart)));
        // easeInOutCubic
        const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

        // Map ramp to glow scale and alpha
        const glowScale = 1 + ease * 3.2;         // halo size multiplier
        const glowAlpha = 0.16 + ease * 0.28;     // halo alpha

        // Pick palette color
        const PALETTE = ['#8fefff', '#6ec6ff', '#55c2ff', '#4fc3f7', '#9be7ff', '#7feaff'];
        const color = PALETTE[Math.floor(Math.random() * PALETTE.length)];

        // size and depth variants
        const depthRoll = Math.random();
        const depthClass = depthRoll < 0.18 ? 'rain-depth-far' : (depthRoll < 0.72 ? 'rain-depth-mid' : 'rain-depth-near');
        const sizeCategoryRoll = Math.random();
        const sizeClass = sizeCategoryRoll < 0.42 ? 'small' : (sizeCategoryRoll < 0.86 ? 'medium' : 'large');
        const baseSize = sizeClass === 'small' ? (Math.random() * 4 + 8) : sizeClass === 'medium' ? (Math.random() * 4 + 12) : (Math.random() * 6 + 18);
        const size = Math.round(baseSize);

        // durations for fall animation (near faster, far slower)
        const duration = depthClass === 'rain-depth-far' ? (Math.random() * 1.8 + 4.6) : depthClass === 'rain-depth-mid' ? (Math.random() * 1.4 + 3.2) : (Math.random() * 1.2 + 1.8);

        const left = (Math.random() * 108) - 4; // -4%..104%
        const angle = (Math.random() * 18 - 24) + 'deg';
        const drift = ((Math.random() < 0.5 ? -1 : 1) * (Math.random() * 78 + 18)) + 'px';
        const blur = depthClass === 'rain-depth-far' ? (Math.random() * 1.4 + 0.8) + 'px' : depthClass === 'rain-depth-mid' ? (Math.random() * 0.6 + 0.3) + 'px' : '0px';

        // Create element
        const drop = document.createElement('div');
        drop.className = `halo-drop ${depthClass} ${sizeClass}`;

        const tail = document.createElement('div');
        tail.className = 'tail';
        drop.appendChild(tail);

        drop.style.setProperty('--left', left + '%');
        drop.style.setProperty('--size', size + 'px');
        drop.style.setProperty('--color', color);
        drop.style.setProperty('--duration', duration + 's');
        drop.style.setProperty('--angle', angle);
        drop.style.setProperty('--drift', drift);
        drop.style.setProperty('--blur', blur);

        // glow variables
        const glowPx = Math.max(10, Math.round(size * glowScale));
        drop.style.setProperty('--glow', glowPx + 'px');
        drop.style.setProperty('--glow-color', hexToRgba(color, glowAlpha));

        // small negative delay for variety
        drop.style.setProperty('--delay', (Math.random() * -0.6).toFixed(2) + 's');

        // store intensity for debugging
        drop.dataset.rampIntensity = ease.toFixed(3);

        return drop;
    }

    // helper hex->rgba used by createRaindrop
    function hexToRgba(hex, alpha = 0.22) {
        const h = hex.replace('#', '');
        const hexFull = h.length === 3 ? h.split('').map(s => s + s).join('') : h;
        const bigint = parseInt(hexFull, 16);
        const r = (bigint >> 16) & 255;
        const g = (bigint >> 8) & 255;
        const b = bigint & 255;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
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