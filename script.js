// The Mirror's Echo - Interactive Script

document.addEventListener('DOMContentLoaded', function() {
    const mirror = document.getElementById('mirror');
    const echoBtn = document.getElementById('echoBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    let echoCount = 0;
    
    // Watermark overlay initialization
    initWatermarkOverlay();
    
    // Create ripple effect on mirror click
    mirror.addEventListener('click', function(e) {
        createRipple(e);
    });
    
    // Echo button functionality
    echoBtn.addEventListener('click', function() {
        createMultipleRipples();
        echoCount++;
        
        // Change mirror appearance based on echo count
        if (echoCount % 5 === 0) {
            const hue = (echoCount * 30) % 360;
            mirror.style.background = `radial-gradient(circle, 
                hsl(${hue}, 70%, 10%), 
                #0a0a0a)`;
            mirror.style.borderColor = `hsl(${hue}, 70%, 50%)`;
        }
    });
    
    // Clear button functionality
    clearBtn.addEventListener('click', function() {
        mirror.style.background = "#0a0a0a";
        mirror.style.borderColor = "#ffffff";
        echoCount = 0;
        
        // Visual feedback
        mirror.style.transform = "scale(0.95)";
        setTimeout(() => {
            mirror.style.transform = "scale(1)";
        }, 200);
    });
    
    function createRipple(event) {
        // Create main ripple ring
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        
        const rect = mirror.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const size = 60;
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = size + 'px';
        ripple.style.height = size + 'px';
        
        mirror.appendChild(ripple);
        
        // Create pulse effect
        const pulse = document.createElement('span');
        pulse.classList.add('ripple', 'pulse');
        pulse.style.left = x + 'px';
        pulse.style.top = y + 'px';
        pulse.style.width = size + 'px';
        pulse.style.height = size + 'px';
        
        mirror.appendChild(pulse);
        
        setTimeout(() => {
            ripple.remove();
        }, 1200);
        
        setTimeout(() => {
            pulse.remove();
        }, 800);
    }
    
    function createMultipleRipples() {
        const count = 8;
        const rect = mirror.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const radius = Math.min(rect.width, rect.height) / 2 * 0.7;
        
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                // Create ripples in a circular pattern for better distribution
                const angle = (i / count) * Math.PI * 2;
                const distance = radius * (0.3 + Math.random() * 0.7);
                const x = centerX + Math.cos(angle) * distance;
                const y = centerY + Math.sin(angle) * distance;
                
                const fakeEvent = {
                    clientX: x,
                    clientY: y
                };
                createRipple(fakeEvent);
            }, i * 100);
        }
    }
    
    // Add ambient breathing animation using requestAnimationFrame
    let animationFrameId;
    function animateMirror() {
        if (echoCount > 0) {
            // Smooth breathing effect with better amplitude
            const time = Date.now() / 2000;
            const scale = 1 + Math.sin(time) * 0.025 + Math.sin(time * 0.7) * 0.01;
            mirror.style.transform = `scale(${scale})`;
            animationFrameId = requestAnimationFrame(animateMirror);
        }
    }
    
    // Start animation when echo count changes
    let lastEchoCount = 0;
    function checkAnimation() {
        if (echoCount > 0 && lastEchoCount === 0) {
            animateMirror();
        } else if (echoCount === 0 && lastEchoCount > 0) {
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        }
        lastEchoCount = echoCount;
    }
    
    // Update animation state when buttons are clicked
    echoBtn.addEventListener('click', () => setTimeout(checkAnimation, 0));
    clearBtn.addEventListener('click', () => setTimeout(checkAnimation, 0));
    
    // Easter egg: Konami code
    let konamiCode = [];
    const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.key);
        konamiCode = konamiCode.slice(-10);
        
        if (konamiCode.join(',') === konamiSequence.join(',')) {
            activateEasterEgg();
        }
    });
    
    function activateEasterEgg() {
        echoText.textContent = "✨ You've unlocked the secret echo! ✨";
        mirror.style.background = "linear-gradient(145deg, gold, orange)";
        createMultipleRipples();
        
        // Create sparkle effect
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.style.left = Math.random() * window.innerWidth + 'px';
                sparkle.style.top = Math.random() * window.innerHeight + 'px';
                document.body.appendChild(sparkle);
                
                setTimeout(() => sparkle.remove(), 2000);
            }, i * 50);
        }
    }
    
    // Watermark overlay functionality
    function initWatermarkOverlay() {
        // Create watermark overlay container
        const overlay = document.createElement('div');
        overlay.className = 'watermark-overlay';
        overlay.id = 'watermarkOverlay';
        
        // Create the static ring
        const ring = document.createElement('div');
        ring.className = 'watermark-ring';
        overlay.appendChild(ring);
        
        // Add overlay to body
        document.body.appendChild(overlay);
        
        // Set timer to show watermark after 7 minutes (420000 ms)
        // For testing, use shorter duration: 10000 ms (10 seconds)
        const WATERMARK_DELAY = 420000; // 7 minutes
        
        setTimeout(() => {
            overlay.classList.add('active');
            startRaindropAnimation(ring);
        }, WATERMARK_DELAY);
    }
    
    function startRaindropAnimation(ringElement) {
        const ringRect = ringElement.getBoundingClientRect();
        const centerX = ringRect.width / 2;
        const centerY = ringRect.height / 2;
        const radius = ringRect.width / 2 - 20; // Keep raindrops inside the ring
        
        let activeRaindrops = [];
        
        function createRaindrop() {
            // Limit number of concurrent raindrops
            if (activeRaindrops.length >= 6) {
                return;
            }
            
            const raindrop = document.createElement('div');
            raindrop.className = 'watermark-raindrop';
            
            // Random position inside the ring
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * radius * 0.8;
            const x = centerX + Math.cos(angle) * distance;
            const y = centerY + Math.sin(angle) * distance;
            
            // Random size between 10-30px
            const size = 10 + Math.random() * 20;
            raindrop.style.width = size + 'px';
            raindrop.style.height = size + 'px';
            raindrop.style.left = x + 'px';
            raindrop.style.top = y + 'px';
            
            // Random duration between 3-6 seconds
            const duration = 3 + Math.random() * 3;
            raindrop.style.animation = `raindrop ${duration}s ease-in-out`;
            
            ringElement.appendChild(raindrop);
            activeRaindrops.push(raindrop);
            
            // Remove after animation completes
            setTimeout(() => {
                raindrop.remove();
                activeRaindrops = activeRaindrops.filter(r => r !== raindrop);
            }, duration * 1000);
        }
        
        // Create initial raindrops
        const initialCount = 3 + Math.floor(Math.random() * 4); // 3-6 raindrops
        for (let i = 0; i < initialCount; i++) {
            setTimeout(() => createRaindrop(), i * 800);
        }
        
        // Continuously create new raindrops at random intervals
        function scheduleNextRaindrop() {
            const delay = 2000 + Math.random() * 3000; // 2-5 seconds
            setTimeout(() => {
                createRaindrop();
                scheduleNextRaindrop();
            }, delay);
        }
        
        scheduleNextRaindrop();
    }
});
