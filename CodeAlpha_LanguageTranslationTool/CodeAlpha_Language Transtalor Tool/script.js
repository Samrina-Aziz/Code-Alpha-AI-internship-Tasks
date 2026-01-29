 // Function to translate text using the backend API
        async function translateText() {
            const inputText = document.getElementById('inputText').value.trim();
            const sourceLang = document.getElementById('sourceLanguage').value;
            const targetLang = document.getElementById('targetLanguage').value;
            const outputText = document.getElementById('outputText');
            const loading = document.getElementById('loading');
            const status = document.getElementById('status');

            // Validation
            if (!inputText) {
                showStatus('Please enter some text to translate!', 'error');
                return;
            }

            if (sourceLang === targetLang) {
                showStatus('Source and target languages must be different!', 'error');
                return;
            }

            // Show loading
            loading.classList.add('active');
            status.style.display = 'none';
            outputText.value = '';

            try {
                // Make API call to Python backend
                const response = await fetch('http://localhost:5000/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: inputText,
                        source_lang: sourceLang,
                        target_lang: targetLang
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    outputText.value = data.translated_text;
                    showStatus('Translation successful!', 'success');
                } else {
                    showStatus(`Error: ${data.error}`, 'error');
                }
            } catch (error) {
                showStatus('Connection error! Make sure the Python server is running.', 'error');
                console.error('Error:', error);
            } finally {
                loading.classList.remove('active');
            }
        }

        // Function to copy translated text to clipboard
        function copyTranslation() {
            const outputText = document.getElementById('outputText');
            
            if (!outputText.value) {
                showStatus('Nothing to copy!', 'error');
                return;
            }

            outputText.select();
            document.execCommand('copy');
            showStatus('Copied to clipboard!', 'success');
        }

        // Function to speak the translated text (Text-to-Speech)
        function speakTranslation() {
            const outputText = document.getElementById('outputText').value;
            const targetLang = document.getElementById('targetLanguage').value;

            if (!outputText) {
                showStatus('Nothing to speak!', 'error');
                return;
            }

            // Check if browser supports speech synthesis
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(outputText);
                utterance.lang = targetLang;
                speechSynthesis.speak(utterance);
                showStatus('Speaking...', 'success');
            } else {
                showStatus('Text-to-speech not supported in this browser!', 'error');
            }
        }

        // Function to clear all text
        function clearAll() {
            document.getElementById('inputText').value = '';
            document.getElementById('outputText').value = '';
            document.getElementById('status').style.display = 'none';
        }

        // Helper function to show status messages
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';

            // Auto-hide after 3 seconds
            setTimeout(() => {
                status.style.display = 'none';
            }, 3000);
        }

        // Allow Enter key to trigger translation
        document.getElementById('inputText').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                translateText();
            }
        });