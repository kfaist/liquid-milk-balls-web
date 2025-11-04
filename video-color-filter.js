// Video Color Filter System
// Click video 5 times to cycle through color lens filters

(function() {
    'use strict';

    let clickCount = 0;
    let currentFilterIndex = 0;

    // Color filter presets (like film camera lens filters)
    const colorFilters = [
        { name: 'Normal', hue: 0, saturation: 100, brightness: 100, contrast: 100 },
        { name: 'Warm', hue: 30, saturation: 120, brightness: 105, contrast: 105 },
        { name: 'Cool', hue: 200, saturation: 110, brightness: 100, contrast: 100 },
        { name: 'Vintage', hue: 20, saturation: 80, brightness: 95, contrast: 110 },
        { name: 'Vivid', hue: 0, saturation: 150, brightness: 110, contrast: 120 },
        { name: 'Noir', hue: 0, saturation: 0, brightness: 90, contrast: 130 },
        { name: 'Sepia', hue: 35, saturation: 50, brightness: 95, contrast: 100 },
        { name: 'Cyberpunk', hue: 280, saturation: 140, brightness: 105, contrast: 115 },
        { name: 'Retro', hue: 340, saturation: 90, brightness: 100, contrast: 95 },
        { name: 'Dreamy', hue: 180, saturation: 80, brightness: 115, contrast: 85 },
        { name: 'Sunset', hue: 15, saturation: 130, brightness: 100, contrast: 105 },
        { name: 'Arctic', hue: 190, saturation: 120, brightness: 110, contrast: 100 }
    ];

    function applyFilter(videoElement) {
        const filter = colorFilters[currentFilterIndex];

        videoElement.style.filter = `
            hue-rotate(${filter.hue}deg)
            saturate(${filter.saturation}%)
            brightness(${filter.brightness}%)
            contrast(${filter.contrast}%)
        `;

        // Show filter name notification
        showFilterNotification(videoElement, filter.name);
    }

    function showFilterNotification(videoElement, filterName) {
        // Remove existing notification if any
        const existing = videoElement.parentElement.querySelector('.filter-notification');
        if (existing) existing.remove();

        // Create notification
        const notification = document.createElement('div');
        notification.className = 'filter-notification';
        notification.textContent = `📷 ${filterName} Filter`;
        videoElement.parentElement.appendChild(notification);

        // Remove after 2 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 500);
        }, 2000);
    }

    function handleVideoClick(videoElement, event) {
        clickCount++;

        // Show click ripple effect
        createClickRipple(videoElement, event);

        // Every 5 clicks, change the filter
        if (clickCount >= 5) {
            clickCount = 0;
            currentFilterIndex = (currentFilterIndex + 1) % colorFilters.length;
            applyFilter(videoElement);
        }

        // Show click counter
        showClickCounter(videoElement, clickCount);
    }

    function createClickRipple(videoElement, event) {
        const ripple = document.createElement('div');
        ripple.className = 'video-click-ripple';

        const rect = videoElement.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';

        videoElement.parentElement.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    function showClickCounter(videoElement, count) {
        // Remove existing counter if any
        const existing = videoElement.parentElement.querySelector('.click-counter');
        if (existing) existing.remove();

        // Create counter
        const counter = document.createElement('div');
        counter.className = 'click-counter';
        counter.textContent = `${count}/5`;
        videoElement.parentElement.appendChild(counter);

        // Remove after 1 second
        setTimeout(() => {
            counter.classList.add('fade-out');
            setTimeout(() => counter.remove(), 300);
        }, 1000);
    }

    function initVideoFilters() {
        // Initialize for local video
        const localVideo = document.getElementById('localVideo');
        if (localVideo) {
            localVideo.style.cursor = 'pointer';
            localVideo.addEventListener('click', (e) => handleVideoClick(localVideo, e));
        }

        // Initialize for remote video
        const remoteVideo = document.getElementById('remoteVideo');
        if (remoteVideo) {
            remoteVideo.style.cursor = 'pointer';
            remoteVideo.addEventListener('click', (e) => handleVideoClick(remoteVideo, e));
        }

        // Initialize for fullscreen video
        const fullscreenVideo = document.getElementById('fullscreenVideo');
        if (fullscreenVideo) {
            fullscreenVideo.style.cursor = 'pointer';
            fullscreenVideo.addEventListener('click', (e) => handleVideoClick(fullscreenVideo, e));
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initVideoFilters);
    } else {
        initVideoFilters();
    }
})();
