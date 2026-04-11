const socket = io();
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
let isPaused = false;
let statusElement = null;

recognition.continuous = true;
recognition.interimResults = true;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle form inputs
    const loginInputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    statusElement = document.createElement('div');
    statusElement.className = 'text-center text-xs text-blue-500 mt-4';
    statusElement.id = 'voice-status';
    
    const form = document.querySelector('form');
    if (form) {
        form.appendChild(statusElement);
    }

    loginInputs.forEach(input => {
        input.addEventListener('focus', () => {
            isPaused = true;
            recognition.stop();
            if (statusElement) statusElement.innerText = "Voice Paused (Typing Mode)";
        });
    });

    loginInputs.forEach(input => {
        input.addEventListener('blur', () => {
            setTimeout(() => {
                if (!document.activeElement.matches('input[type="text"], input[type="password"]')) {
                    resumeVoice();
                }
            }, 100);
        });
    });

    // Start voice recognition
    setTimeout(() => {
        resumeVoice();
    }, 1000);
});

function resumeVoice() {
    isPaused = false;
    if (statusElement) statusElement.innerText = "Listening for commands...";
    try {
        recognition.start();
    } catch (e) {
        console.log('Recognition already started');
    }
}

function fillField(fieldName, value) {
    const field = document.querySelector(`input[name="${fieldName}"]`);
    if (field) {
        field.value = value;
        if (statusElement) statusElement.innerText = `Filled ${fieldName}: ${value}`;
    }
}

function submitForm() {
    const form = document.querySelector('form');
    if (form) {
        form.submit();
    }
}

recognition.onresult = (event) => {
    if (isPaused) return;

    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript.toLowerCase().trim();
            processCommand(finalTranscript);
        } else {
            interimTranscript += event.results[i][0].transcript;
        }
    }
    
    if (interimTranscript && statusElement) {
        statusElement.innerText = `Listening: ${interimTranscript}`;
    }
};

function processCommand(command) {
    const isLoginPage = window.location.pathname === '/' || window.location.pathname.includes('login');
    
    // Handle field filling
    if (command.includes('username') || command.includes('name')) {
        const match = command.match(/(?:username|name)\s+(.+)/);
        if (match) {
            fillField('username', match[1].trim());
        }
    } else if (command.includes('password')) {
        const match = command.match(/password\s+(.+)/);
        if (match) {
            fillField('password', match[1].trim());
        }
    }
    
    // Handle form submission
    if (command.includes('submit') || command.includes('login') || command.includes('sign in')) {
        if (isLoginPage) {
            submitForm();
        }
    } else if (command.includes('register') || command.includes('create account') || command.includes('sign up')) {
        if (!isLoginPage) {
            submitForm();
        }
    }
    
    // Handle navigation
    if (command.includes('go to register') || command.includes('create account')) {
        if (isLoginPage) {
            window.location.href = '/register';
        }
    } else if (command.includes('go to login') || command.includes('sign in')) {
        if (!isLoginPage) {
            window.location.href = '/';
        }
    }
    
    // Handle Google auth
    if (command.includes('google') || command.includes('sign in with google')) {
        window.location.href = '/auth/google';
    }
    
    // Handle stop
    if (command.includes('stop')) {
        if (statusElement) statusElement.innerText = "Goodbye!";
        setTimeout(() => {
            window.close();
            window.location.href = 'about:blank';
        }, 1000);
    }
}

recognition.onend = () => {
    console.log('Auth recognition ended');
    if (!isPaused) {
        try {
            recognition.start();
            console.log('Auth recognition restarted');
        } catch (e) {
            console.log('Failed to restart auth recognition:', e);
            // Try to restart after a delay
            setTimeout(() => {
                try {
                    recognition.start();
                    console.log('Auth recognition restarted after delay');
                } catch (e2) {
                    console.log('Failed to restart auth recognition after delay:', e2);
                }
            }, 1000);
        }
    }
};

// Add error handling for auth
recognition.onerror = (event) => {
    console.log('Auth recognition error:', event.error);
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

// Handle UI updates from server
socket.on('ui_update', (data) => {
    if (statusElement) statusElement.innerText = data.msg;
});

// Add heartbeat to keep recognition alive
setInterval(() => {
    if (!isPaused && recognition) {
        try {
            // Check if recognition is still running
            if (recognition.readyState !== 'active') {
                console.log('Auth recognition not active, restarting...');
                recognition.start();
            }
        } catch (e) {
            console.log('Auth heartbeat restart failed:', e);
        }
    }
}, 5000); // Check every 5 seconds
