const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
const synth = window.speechSynthesis;
let isListening = false;

recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.voice = synth.getVoices().find(voice => voice.lang === 'en-US') || synth.getVoices()[0];
    synth.speak(utterance);
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}

function updateOutput(message) {
    document.getElementById('output').textContent = message;
}

async function processCommand(command) {
    const response = await fetch('/process_command/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
    });
    const data = await response.json();

    updateOutput(`Recognized: ${command}`);
    updateStatus(data.status);
    if (data.speak) {
        speak(data.message);
    }
    if (data.open_url) {
        window.open(data.open_url, '_blank');
    }
    if (data.stop_recognition) {
        recognition.stop();
        isListening = false;
        updateStatus('Press and hold the spacebar to speak to Jarvis');
    }
}

recognition.onresult = (event) => {
    const command = event.results[0][0].transcript.toLowerCase();
    isListening = false;
    processCommand(command);
};

recognition.onerror = (event) => {
    isListening = false;
    updateStatus('Error in recognition: ' + event.error);
};

recognition.onend = () => {
    isListening = false;
    updateStatus('Press and hold the spacebar to speak to Jarvis');
};

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && !isListening && !event.repeat) {
        event.preventDefault(); // Prevent spacebar scrolling
        recognition.start();
        isListening = true;
        updateStatus('Listening...');
    }
});

document.addEventListener('keyup', (event) => {
    if (event.code === 'Space' && isListening) {
        recognition.stop();
        isListening = false;
        updateStatus('Press and hold the spacebar to speak to Jarvis');
    }
});

// Initial greeting
window.onload = async () => {
    const response = await fetch('/initialize/');
    const data = await response.json();
    updateStatus(data.status);
    updateOutput(data.message);
    if (data.speak) {
        speak(data.message);
    }
};