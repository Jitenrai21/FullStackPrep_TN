const API_URL = "/chat/"; // Django endpoint

window.chatAPI = {
    init: function() {
        console.log("chatAPI.init called");
        // Generate UUID for session
        const sessionId = this.generateUUID();
        console.log("Session ID:", sessionId);

        // Check SpeechRecognition support
        const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let isListening = false;

        if (!recognition) {
            console.log("SpeechRecognition not supported");
            const micBtn = document.getElementById("mic-btn");
            if (micBtn) {
                micBtn.disabled = true;
                micBtn.title = "Voice input not supported in this browser";
            }
            const voiceStatus = document.getElementById("voice-status");
            if (voiceStatus) {
                voiceStatus.textContent = "Voice input is not supported in this browser.";
                voiceStatus.classList.remove("hidden");
            }
        } else {
            const recognizer = new recognition();
            recognizer.interimResults = true;
            recognizer.lang = 'en-US';

            recognizer.onresult = (event) => {
                console.log("SpeechRecognition result received");
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                const userInput = document.getElementById("user-input");
                if (userInput) userInput.value = transcript;
                const voiceStatus = document.getElementById("voice-status");
                if (voiceStatus) voiceStatus.textContent = "Listening... (Speak clearly)";
            };

            recognizer.onend = () => {
                console.log("SpeechRecognition ended");
                isListening = false;
                const micBtn = document.getElementById("mic-btn");
                if (micBtn) micBtn.classList.remove("listening");
                const voiceStatus = document.getElementById("voice-status");
                if (voiceStatus) voiceStatus.classList.add("hidden");
                const userInput = document.getElementById("user-input");
                if (userInput && userInput.value.trim()) {
                    this.sendMessage(sessionId, userInput.value.trim());
                }
            };

            recognizer.onerror = (event) => {
                console.log("SpeechRecognition error:", event.error);
                isListening = false;
                const micBtn = document.getElementById("mic-btn");
                if (micBtn) micBtn.classList.remove("listening");
                const voiceStatus = document.getElementById("voice-status");
                if (voiceStatus) voiceStatus.classList.add("hidden");
                const errorMessage = document.getElementById("error-message");
                if (errorMessage) {
                    errorMessage.textContent = `Voice input error: ${event.error}`;
                    errorMessage.classList.remove("hidden");
                }
            };

            const micBtn = document.getElementById("mic-btn");
            if (micBtn) {
                micBtn.addEventListener("click", () => {
                    console.log("Mic button clicked");
                    if (!isListening) {
                        isListening = true;
                        micBtn.classList.add("listening");
                        const voiceStatus = document.getElementById("voice-status");
                        if (voiceStatus) {
                            voiceStatus.textContent = "Listening... (Speak clearly)";
                            voiceStatus.classList.remove("hidden");
                        }
                        recognizer.start();
                    }
                });
            } else {
                console.error("Mic button not found");
            }
        }

        // Check SpeechSynthesis support
        if (!window.speechSynthesis) {
            console.log("SpeechSynthesis not supported");
            const enableSpeech = document.getElementById("enable-speech");
            if (enableSpeech) enableSpeech.disabled = true;
            const speechSupport = document.getElementById("speech-support");
            if (speechSupport) {
                speechSupport.textContent = "Text-to-speech is not supported in this browser.";
                speechSupport.classList.remove("hidden");
            }
        }

        // Set up event listeners
        const sendBtn = document.getElementById("send-btn");
        if (sendBtn) {
            sendBtn.addEventListener("click", () => {
                console.log("Send button clicked");
                const userInput = document.getElementById("user-input");
                if (userInput && userInput.value.trim()) {
                    this.sendMessage(sessionId, userInput.value.trim());
                }
            });
        } else {
            console.error("Send button not found");
        }

        const userInput = document.getElementById("user-input");
        if (userInput) {
            userInput.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    console.log("Enter key pressed");
                    if (userInput.value.trim()) {
                        this.sendMessage(sessionId, userInput.value.trim());
                    }
                }
            });
        } else {
            console.error("User input field not found");
        }
    },

    generateUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    sendMessage: function(sessionId, message) {
        console.log("sendMessage called with:", message);
        const persona = document.getElementById("persona")?.value;
        const errorMessage = document.getElementById("error-message");

        if (!message) {
            console.log("No message provided");
            if (errorMessage) {
                errorMessage.textContent = "Please enter or speak a message.";
                errorMessage.classList.remove("hidden");
            }
            return;
        }

        if (errorMessage) errorMessage.classList.add("hidden");
        this.appendMessage("User", message, "user-message");

        const data = {
            session_id: sessionId,
            persona: persona,
            message: message
        };

        fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            console.log("API response received:", response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("API data:", data);
            this.appendMessage(persona, data.response, "bot-message");
            if (window.speechSynthesis && document.getElementById("enable-speech")?.checked) {
                console.log("Speaking response:", data.response);
                const utterance = new SpeechSynthesisUtterance(data.response);
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }
            const userInput = document.getElementById("user-input");
            if (userInput) userInput.value = "";
            this.scrollToBottom();
        })
        .catch(error => {
            console.error("API error:", error);
            if (errorMessage) {
                errorMessage.textContent = "Error communicating with the server.";
                errorMessage.classList.remove("hidden");
            }
        });
    },

    appendMessage: function(sender, message, className) {
        console.log("Appending message from:", sender);
        const chatOutput = document.getElementById("chat-output");
        if (chatOutput) {
            const messageDiv = document.createElement("div");
            messageDiv.className = `chat-message ${className}`;
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message.replace(/\n/g, "<br>")}`;
            chatOutput.appendChild(messageDiv);
        }
    },

    scrollToBottom: function() {
        console.log("Scrolling to bottom");
        const chatContainer = document.querySelector(".chat-container");
        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
    }
};