// Live Transcription System using Web Speech API
// Updates approximately every 1.2 seconds with speech recognition results

(function() {
    'use strict';

    let recognition = null;
    let isListening = false;
    let transcriptionBuffer = [];
    let lastUpdateTime = 0;
    const UPDATE_INTERVAL = 1200; // 1.2 seconds

    function initTranscription() {
        const toggleBtn = document.getElementById('transcriptionToggle');
        const transcriptionText = document.getElementById('transcriptionText');
        const transcriptionLabel = document.querySelector('.transcription-label');

        if (!toggleBtn || !transcriptionText) return;

        // Check if browser supports Web Speech API
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            transcriptionText.innerHTML = '<span class="transcription-error">⚠️ Speech recognition not supported in this browser. Try Chrome or Edge.</span>';
            toggleBtn.disabled = true;
            return;
        }

        // Initialize recognition
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        recognition.maxAlternatives = 1;

        // Handle recognition results
        recognition.onresult = (event) => {
            const currentTime = Date.now();
            let interimTranscript = '';
            let finalTranscript = '';

            // Process all results
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;

                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update buffer with final results
            if (finalTranscript) {
                transcriptionBuffer.push({
                    text: finalTranscript.trim(),
                    timestamp: currentTime,
                    final: true
                });
            }

            // Update display at intervals (approximately 1.2 seconds)
            if (currentTime - lastUpdateTime >= UPDATE_INTERVAL || finalTranscript) {
                updateTranscriptionDisplay(interimTranscript);
                lastUpdateTime = currentTime;
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);

            if (event.error === 'no-speech') {
                // Don't stop for no-speech, just continue listening
                return;
            }

            if (event.error === 'not-allowed') {
                transcriptionText.innerHTML = '<span class="transcription-error">⚠️ Microphone access denied. Please allow microphone permissions.</span>';
                stopListening();
            }
        };

        recognition.onend = () => {
            // Automatically restart if still supposed to be listening
            if (isListening) {
                try {
                    recognition.start();
                } catch (e) {
                    console.error('Error restarting recognition:', e);
                }
            }
        };

        // Toggle button handler
        toggleBtn.addEventListener('click', () => {
            if (isListening) {
                stopListening();
            } else {
                startListening();
            }
        });

        function startListening() {
            try {
                recognition.start();
                isListening = true;
                toggleBtn.textContent = 'Stop Listening';
                toggleBtn.classList.add('active');

                // Add listening indicator
                const indicator = document.createElement('span');
                indicator.className = 'listening-indicator';
                transcriptionLabel.appendChild(indicator);

                // Clear placeholder
                transcriptionText.innerHTML = '';
                transcriptionBuffer = [];
                lastUpdateTime = Date.now();

            } catch (e) {
                console.error('Error starting recognition:', e);
                transcriptionText.innerHTML = '<span class="transcription-error">⚠️ Could not start listening. Please try again.</span>';
            }
        }

        function stopListening() {
            if (recognition) {
                recognition.stop();
            }
            isListening = false;
            toggleBtn.textContent = 'Start Listening';
            toggleBtn.classList.remove('active');

            // Remove listening indicator
            const indicator = document.querySelector('.listening-indicator');
            if (indicator) {
                indicator.remove();
            }
        }

        function updateTranscriptionDisplay(interimText) {
            const transcriptionText = document.getElementById('transcriptionText');
            if (!transcriptionText) return;

            // Build display HTML
            let html = '';

            // Add final transcripts (keep last 50 words to prevent overflow)
            const recentTranscripts = transcriptionBuffer.slice(-50);
            for (const item of recentTranscripts) {
                const words = item.text.split(' ');
                for (const word of words) {
                    if (word.trim()) {
                        html += `<span class="transcription-word final">${escapeHtml(word)}</span> `;
                    }
                }
            }

            // Add interim (currently speaking) text
            if (interimText) {
                const interimWords = interimText.split(' ');
                for (const word of interimWords) {
                    if (word.trim()) {
                        html += `<span class="transcription-word interim">${escapeHtml(word)}</span> `;
                    }
                }
            }

            transcriptionText.innerHTML = html || '<span class="transcription-placeholder">Listening...</span>';

            // Auto-scroll to bottom
            transcriptionText.scrollTop = transcriptionText.scrollHeight;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTranscription);
    } else {
        initTranscription();
    }
})();
