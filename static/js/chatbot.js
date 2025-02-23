document.addEventListener('DOMContentLoaded', function() {
    const chatbot = document.getElementById('chatbot');
    const minimizeButton = document.getElementById('minimize-chat');
    const messagesContainer = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-message');
    const toggleButton = document.getElementById('chatbot-toggle');

    // Get the current subject from localStorage
    const currentSubject = localStorage.getItem('subject') || 'General';

    // Initially hide the chatbot
    chatbot.style.display = 'none';

    // Add toggle button event listener
    toggleButton.addEventListener('click', () => {
        console.log('Chatbot icon clicked!');
        console.log('Current display:', chatbot.style.display);
        if (chatbot.style.display === 'none' || chatbot.style.display === '') {
            chatbot.style.display = 'flex';
            userInput.focus(); // Focus on input when chatbot opens
        } else {
            chatbot.style.display = 'none';
        }
    });

    // Minimize/Maximize chat
 

    // Send message function
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message
            addMessage(message, 'user');
            
            // Clear input
            userInput.value = '';

            // Show loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot loading';
            loadingDiv.innerHTML = '<p>Typing...</p>';
            messagesContainer.appendChild(loadingDiv);

            try {
                // Send message to backend
                const response = await fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: `Context: User is studying ${currentSubject}. User's question: ${message}`
                    })
                });

                const data = await response.json();
                
                // Remove loading indicator
                messagesContainer.removeChild(loadingDiv);
                
                // Add bot response
                addMessage(data.response, 'bot');
            } catch (error) {
                // Remove loading indicator
                messagesContainer.removeChild(loadingDiv);
                // Add error message
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                console.error('Error:', error);
            }
        }
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        // For bot messages, use the HTML returned from backend (markdown converted)
        // For user messages, escape HTML
        if (sender === 'bot') {
            messageDiv.innerHTML = `<p>${text}</p>`;
        } else {
            const p = document.createElement('p');
            p.textContent = text;
            messageDiv.appendChild(p);
        }
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});