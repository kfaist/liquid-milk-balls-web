// The Mirror's Echo - Interactive Script

document.addEventListener('DOMContentLoaded', function() {
    const mirror = document.getElementById('mirror');
    const echoBtn = document.getElementById('echoBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    let echoCount = 0;
    
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
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        
        const rect = mirror.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        
        mirror.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 1000);
    }
    
    function createMultipleRipples() {
        const count = 8;
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                const fakeEvent = {
                    clientX: mirror.getBoundingClientRect().left + Math.random() * mirror.offsetWidth,
                    clientY: mirror.getBoundingClientRect().top + Math.random() * mirror.offsetHeight
                };
                createRipple(fakeEvent);
            }, i * 80);
        }
    }
    
    // Add ambient animation using requestAnimationFrame
    let animationFrameId;
    function animateMirror() {
        if (echoCount > 0) {
            const scale = 1 + Math.sin(Date.now() / 1500) * 0.015;
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
});
