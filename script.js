// The Mirror's Echo - Interactive Script

document.addEventListener('DOMContentLoaded', function() {
    const mirror = document.getElementById('mirror');
    const echoText = document.getElementById('echoText');
    const echoBtn = document.getElementById('echoBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    const echoMessages = [
        "Your reflection whispers...",
        "Time stands still in the mirror...",
        "What do you see?",
        "The echo remembers...",
        "Look deeper...",
        "Your essence is captured...",
        "The mirror knows your truth...",
        "Reflections never lie...",
        "You are seen...",
        "The echo grows stronger..."
    ];
    
    let echoCount = 0;
    
    // Create ripple effect on mirror click
    mirror.addEventListener('click', function(e) {
        createRipple(e);
        changeEchoText();
    });
    
    // Echo button functionality
    echoBtn.addEventListener('click', function() {
        createMultipleRipples();
        changeEchoText();
        echoCount++;
        
        // Change mirror appearance based on echo count
        if (echoCount % 5 === 0) {
            mirror.style.background = `linear-gradient(145deg, 
                hsl(${echoCount * 10}, 70%, 50%), 
                hsl(${echoCount * 15}, 60%, 40%))`;
        }
    });
    
    // Clear button functionality
    clearBtn.addEventListener('click', function() {
        echoText.textContent = "Look into the mirror...";
        mirror.style.background = "linear-gradient(145deg, #ffffff15, #ffffff05)";
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
        const count = 5;
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                const fakeEvent = {
                    clientX: mirror.getBoundingClientRect().left + Math.random() * mirror.offsetWidth,
                    clientY: mirror.getBoundingClientRect().top + Math.random() * mirror.offsetHeight
                };
                createRipple(fakeEvent);
            }, i * 100);
        }
    }
    
    function changeEchoText() {
        const randomMessage = echoMessages[Math.floor(Math.random() * echoMessages.length)];
        echoText.style.opacity = '0';
        
        setTimeout(() => {
            echoText.textContent = randomMessage;
            echoText.style.opacity = '1';
        }, 300);
    }
    
    // Add ambient animation using requestAnimationFrame
    let animationFrameId;
    function animateMirror() {
        if (echoCount > 0) {
            const scale = 1 + Math.sin(Date.now() / 1000) * 0.02;
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
