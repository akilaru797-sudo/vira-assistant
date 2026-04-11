const socket = io();
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
let isPaused = false;

// Add connection debugging
socket.on('connect', () => {
    console.log('Connected to server with ID:', socket.id);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('connect_error', (error) => {
    console.log('Connection error:', error);
});

recognition.continuous = true;
recognition.interimResults = true;
recognition.maxAlternatives = 1;

// Increase listening time for longer messages
recognition.onstart = () => {
    console.log('Speech recognition started');
    document.getElementById('status').innerText = "Listening...";
};

const inputField = document.getElementById('manual-input');

inputField.addEventListener('focus', () => {
    isPaused = true;
    recognition.stop();
    document.getElementById('status').innerText = "Voice Paused (Typing Mode)";
});

inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const val = inputField.value;
        if (val) {
            socket.emit('voice_command', { text: val });
            inputField.value = "";
        }
        resumeVoice();
    }
});

function resumeVoice() {
    isPaused = false;
    document.getElementById('status').innerText = "Listening...";
    recognition.start();
}

recognition.onresult = (event) => {
    if (isPaused) return;

    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
            console.log('Sending voice command:', finalTranscript);

            // Show input beside listening
            document.getElementById('current-input').innerText = finalTranscript;
            
            // Send to server for processing
            socket.emit('voice_command', { text: finalTranscript });
            
        } else {
            interimTranscript += event.results[i][0].transcript;
        }
    }

    // Show interim transcript in status
    if (interimTranscript) {
        document.getElementById('status').innerText = `Listening: ${interimTranscript}`;
    } else {
        document.getElementById('status').innerText = "Listening...";
    }
};

recognition.onend = () => {
    console.log('Recognition ended');
    if (!isPaused) {
        try {
            recognition.start();
            console.log('Recognition restarted');
        } catch (e) {
            console.log('Failed to restart recognition:', e);
            // Try to restart after a delay
            setTimeout(() => {
                try {
                    recognition.start();
                    console.log('Recognition restarted after delay');
                } catch (e2) {
                    console.log('Failed to restart recognition after delay:', e2);
                }
            }, 1000);
        }
    }
};

// Add error handling
recognition.onerror = (event) => {
    console.log('Recognition error:', event.error);
    if (event.error === 'no-speech') {
        // No speech detected, just restart
        if (!isPaused) {
            setTimeout(() => recognition.start(), 100);
        }
    } else if (event.error === 'network') {
        // Network error, try restart
        if (!isPaused) {
            setTimeout(() => recognition.start(), 2000);
        }
    }
};

// Handle system actions like shutdown and logout
socket.on('sys_action', (data) => {
    if (data.action === 'shutdown') {
        window.close();
        // Fallback for browsers that don't allow window.close()
        window.location.href = 'about:blank';
    } else if (data.action === 'logout') {
        // Redirect to login page after logout
        window.location.href = '/logout';
    }
});

// Add heartbeat to keep recognition alive
setInterval(() => {
    if (!isPaused && recognition) {
        try {
            // Check if recognition is still running
            if (recognition.readyState !== 'active') {
                console.log('Recognition not active, restarting...');
                recognition.start();
            }
        } catch (e) {
            console.log('Heartbeat restart failed:', e);
        }
    }
}, 5000); // Check every 5 seconds

recognition.start();