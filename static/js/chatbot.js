document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function sendMessage() {
        const messageText = userInput.value.trim();

        if (messageText !== '') {
            // Display user message
            displayUserMessage(messageText);

            // Clear the input field
            userInput.value = '';

            // Send message to backend
            fetch('/support/chatbot/api/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
                },
                body: JSON.stringify({ message: messageText })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.reply) {
                        displayBotMessage(data.reply);
                    } else if (data.error) {
                        console.error('Error from bot:', data.error);
                        displayBotMessage('An error occurred.');
                    }
                })
                .catch(error => {
                    console.error('Network error:', error);
                    displayBotMessage('Failed to get a response.');
                });
        }
    }
    function displayUserMessage(messageText){
            const chatBox = document.getElementById('chat-box');

        if (messageText !== '') {
            // Create a new message element for the user's message
            const userMessageElement = document.createElement('div');
            userMessageElement.classList.add('chat-message', 'user-message');
            userMessageElement.textContent = messageText;

            // Add the message to the chat box
            chatBox.appendChild(userMessageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    function displayBotMessage(messageText) {
        const chatBox = document.getElementById('chat-box');
        // Create a new message element for the bot's message
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('chat-message', 'bot-message');
        botMessageElement.textContent = messageText;

        // Add the message to the chat box
        chatBox.appendChild(botMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function getCookie(name) {
        // This function retrieves the CSRF token from cookies
        // ... (Implementation of getCookie is required)
        return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
    }

    // Event listener for the send button
    sendButton.addEventListener('click', sendMessage);

    // Event listener for the enter key in the input field
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default form submission
            sendMessage();
        }
    });
});