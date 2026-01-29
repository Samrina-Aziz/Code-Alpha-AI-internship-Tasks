"""
FAQ Chatbot Backend - app.py
This is the main Python file that runs the chatbot server and handles AI logic.

Key Concepts:
1. NLP Preprocessing: Cleaning text data (lowercase, remove punctuation, remove stopwords)
2. TF-IDF: Converts text into numerical vectors based on word importance
3. Cosine Similarity: Measures how similar two text vectors are (0 = different, 1 = identical)
"""

from flask import Flask, render_template, request, jsonify
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re

# Download required NLTK data (run once)
print("Checking NLTK data...")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords...")
    nltk.download('stopwords')
    
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading punkt_tab...")
    nltk.download('punkt_tab')

print("NLTK data ready!")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Initialize Flask app
app = Flask(__name__)

# Load FAQ data from JSON file
with open('faqs.json', 'r') as f:
    faq_data = json.load(f)

# Extract questions and answers into separate lists
faq_questions = [item['question'] for item in faq_data['faqs']]
faq_answers = [item['answer'] for item in faq_data['faqs']]


def preprocess_text(text):
    """
    Clean and prepare text for NLP processing.
    
    Steps:
    1. Convert to lowercase (so "Hello" and "hello" are treated the same)
    2. Remove punctuation marks (!, ?, ., etc.)
    3. Tokenize (split text into individual words)
    4. Remove stopwords (common words like "the", "is", "a" that don't add meaning)
    
    Args:
        text (str): Raw input text
    
    Returns:
        str: Cleaned text ready for analysis
    """
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Remove punctuation
    # Create a translation table that maps each punctuation to None (removes it)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    # Step 3: Tokenization - split text into words
    tokens = word_tokenize(text)
    
    # Step 4: Remove stopwords (common words that don't carry much meaning)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Join the cleaned words back into a single string
    return ' '.join(filtered_tokens)


def find_best_match(user_question, threshold=0.3):
    """
    Find the most similar FAQ to the user's question using TF-IDF and cosine similarity.
    
    How it works:
    1. Preprocess user question and all FAQ questions
    2. Use TF-IDF to convert text into numerical vectors
    3. Calculate cosine similarity between user question and each FAQ
    4. Return the answer with highest similarity score
    
    Args:
        user_question (str): The question asked by the user
        threshold (float): Minimum similarity score (0-1) to return a match
    
    Returns:
        dict: Contains 'answer', 'similarity_score', and 'matched_question'
    """
    # Preprocess the user's question
    processed_user_question = preprocess_text(user_question)
    
    # Preprocess all FAQ questions
    processed_faq_questions = [preprocess_text(q) for q in faq_questions]
    
    # Create TF-IDF vectorizer
    # TF-IDF = Term Frequency - Inverse Document Frequency
    # It gives higher weight to words that are rare but important
    vectorizer = TfidfVectorizer()
    
    # Fit the vectorizer on FAQ questions and transform them into vectors
    # We include the user question in the same transformation to ensure consistency
    all_questions = processed_faq_questions + [processed_user_question]
    tfidf_matrix = vectorizer.fit_transform(all_questions)
    
    # Separate the user question vector from FAQ vectors
    faq_vectors = tfidf_matrix[:-1]  # All except last
    user_vector = tfidf_matrix[-1]    # Last one is user question
    
    # Calculate cosine similarity between user question and each FAQ
    # Cosine similarity ranges from 0 (completely different) to 1 (identical)
    similarities = cosine_similarity(user_vector, faq_vectors)[0]
    
    # Find the index of the most similar FAQ
    best_match_index = similarities.argmax()
    best_similarity_score = similarities[best_match_index]
    
    # Check if the best match is above the threshold
    if best_similarity_score >= threshold:
        return {
            'answer': faq_answers[best_match_index],
            'similarity_score': float(best_similarity_score),
            'matched_question': faq_questions[best_match_index]
        }
    else:
        # No good match found
        return {
            'answer': "I'm sorry, I couldn't find a relevant answer to your question. Please try rephrasing or contact our support team for assistance.",
            'similarity_score': float(best_similarity_score),
            'matched_question': None
        }


# Route for home page
@app.route('/')
def home():
    """
    Serve the main chatbot interface (index.html)
    """
    return render_template('index.html')


# API endpoint for chatbot responses
@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle incoming chat messages from the frontend.
    
    This endpoint:
    1. Receives user question as JSON
    2. Processes it through the chatbot logic
    3. Returns the best matching answer
    """
    try:
        # Get the user's question from the request
        data = request.get_json()
        user_question = data.get('question', '')
        
        # Validate input
        if not user_question.strip():
            return jsonify({
                'error': 'Please enter a question'
            }), 400
        
        # Find the best matching FAQ answer
        result = find_best_match(user_question)
        
        # Return the response as JSON
        return jsonify({
            'answer': result['answer'],
            'confidence': result['similarity_score'],
            'matched_question': result['matched_question']
        })
    
    except Exception as e:
        # Handle any errors gracefully
        print(f"Error occurred: {str(e)}")  # Log error to console
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500


# Run the Flask application
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Starting FAQ Chatbot Server...")
    print("="*50)
    print("Visit http://127.0.0.1:5000 in your browser")
    print("Press CTRL+C to quit")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)