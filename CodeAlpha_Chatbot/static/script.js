/*
   Chatbot Frontend Logic - script.js
   This file handles user interactions and communicates with the Python backend
*/

// Wait for the page to fully load before running JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Get references to HTML elements we'll need
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const confidenceDisplay = document.getElementById('confidenceDisplay');
    
    /**
     * Add a message to the chat interface
     * @param {string} text - The message text to display
     * @param {string} sender - Either 'user' or 'bot'
     */
    function addMessage(text, sender) {
        // Create a new message div
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        // Create the message content div
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Create a paragraph for the text
        const p = document.createElement('p');
        p.textContent = text;
        
        // Assemble the message structure
        contentDiv.appendChild(p);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll to the bottom to show the new message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Show a loading indicator while waiting for bot response
     */
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message';
        loadingDiv.id = 'loadingMessage';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const p = document.createElement('p');
        p.innerHTML = 'Thinking<span class="loading"></span>';
        
        contentDiv.appendChild(p);
        loadingDiv.appendChild(contentDiv);
        chatMessages.appendChild(loadingDiv);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Remove the loading indicator
     */
    function hideLoading() {
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    /**
     * Update the confidence score display
     * @param {number} confidence - Similarity score from 0 to 1
     */
    function updateConfidence(confidence) {
        if (confidence) {
            const percentage = (confidence * 100).toFixed(1);
            let message = 'High confidence';
            
            // Determine confidence level
            if (confidence < 0.3) {
                message = 'Low confidence - answer may not be accurate';
            } else if (confidence < 0.6) {
                message = 'Medium confidence';
            }
            
            confidenceDisplay.textContent = `${emoji} ${message} (${percentage}%)`;
        } else {
            confidenceDisplay.textContent = '';
        }
    }
    
    /**
     * Send user question to the backend and get bot response
     * This is where the frontend communicates with the Python Flask server
     */
    async function sendMessage() {
        // Get the user's input
        const question = userInput.value.trim();
        
        // Don't send empty messages
        if (!question) {
            return;
        }
        
        // Display user's message in the chat
        addMessage(question, 'user');
        
        // Clear the input field
        userInput.value = '';
        
        // Disable input while processing
        userInput.disabled = true;
        sendButton.disabled = true;
        
        // Show loading indicator
        showLoading();
        
        try {
            // Send POST request to the backend /chat endpoint
            // This is how JavaScript communicates with Python Flask
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });
            
            // Parse the JSON response from the backend
            const data = await response.json();
            
            // Hide loading indicator
            hideLoading();
            
            // Check if request was successful
            if (response.ok) {
                // Display bot's answer
                addMessage(data.answer, 'bot');
                
                // Update confidence score
                updateConfidence(data.confidence);
                
                // Optional: Show which FAQ was matched (for debugging/transparency)
                if (data.matched_question) {
                    console.log('Matched FAQ:', data.matched_question);
                }
            } else {
                // Handle error response
                addMessage(data.error || 'Sorry, something went wrong.', 'bot');
            }
            
        } catch (error) {
            // Handle network or other errors
            hideLoading();
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            console.error('Error:', error);
        } finally {
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }
    
    // Event listener: Send message when button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Event listener: Send message when Enter key is pressed
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Focus on input field when page loads
    userInput.focus();
});