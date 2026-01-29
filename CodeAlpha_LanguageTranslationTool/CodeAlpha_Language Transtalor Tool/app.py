from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the HTML frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({'message': 'Translation API is running!', 'status': 'ok'})

@app.route('/translate', methods=['POST'])
def translate():
    """
    Endpoint to handle translation requests
    Expects JSON with: text, source_lang, target_lang
    Returns: translated_text or error message
    """
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'es')
        
        # Check if text is provided
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Log the translation request
        logger.info(f"Translating from {source_lang} to {target_lang}: {text[:50]}...")
        
        translated_text = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)
        
        # Return the translated text
        return jsonify({
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }), 200
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    """
    Endpoint to get list of supported languages
    """
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-cn': 'Chinese (Simplified)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ur': 'Urdu'
    }
    return jsonify(languages), 200

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy', 'message': 'Translation API is running'}), 200

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Starting Translation Server...")
    print("=" * 50)
    print("Server running on http://localhost:5000")
    print("Open index.html in your browser to use the app")
    print("Using deep-translator (GoogleTranslator)")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)