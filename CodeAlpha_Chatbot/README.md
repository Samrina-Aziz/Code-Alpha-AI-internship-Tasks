# AI FAQ Chatbot Assistant

A professional full-stack web application designed to serve as an AI-driven FAQ Chatbot. This project utilizes a Python Flask backend employing Natural Language Processing (NLP) techniques like TF-IDF and Cosine Similarity to provide intelligent responses based on a structured dataset.

---

## Features

* **AI-Driven Responses:** Uses TF-IDF vectorization and Cosine Similarity to find the most relevant answers from a predefined FAQ dataset.
* **Real-time Confidence Scoring:** Displays a confidence percentage for each response to indicate how closely the user's question matched the FAQ data.
* **NLP Preprocessing:** Automatically cleans input by converting text to lowercase, removing punctuation, and filtering out common stopwords.
* **Responsive Chat Interface:** Features a modern, mobile-friendly design with animated message bubbles and auto-scrolling functionality.
* **Smart Validation:** Validates user input and manages server-side errors gracefully with informative status messages.

---

## Technical Stack

### Backend

* **Python/Flask:** Serves as the primary web server and API manager.
* **NLTK (Natural Language Toolkit):** Handles text tokenization and stopword removal.
* **Scikit-learn:** Provides the `TfidfVectorizer` for numerical text conversion and `cosine_similarity` for match calculation.

### Frontend

* **HTML5:** Provides a semantic chat container and input structure.
* **CSS3:** Implements a professional linear-gradient UI, message animations, and a responsive layout.
* **JavaScript (ES6+):** Manages asynchronous communication with the backend via the Fetch API and handles DOM updates.

---

## Project Structure

```text
CodeAlpha_Chatbot/
│
├── static/
│   ├── script.js        # Frontend logic and API communication
│   └── style.css        # UI styling and animations
├── templates/
│   └── index.html       # Main chatbot interface
├── app.py               # Flask backend and AI/NLP logic
├── faqs.json            # Structured dataset of questions and answers
├── requirements.txt     # Python dependency list
└── README.md            # Project documentation

```

---

## Installation and Setup

### 1. Environment Preparation

It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

```

### 2. Install Dependencies

Install the required packages as defined in the project configuration:

```bash
pip install -r requirements.txt

```

### 3. Run the Application

Start the Flask server:

```bash
python app.py

```

The server will start on `http://127.0.0.1:5000`. Open this URL in your browser to access the chatbot interface.

---

## API Documentation

### Chat Endpoint

Handles incoming user questions and returns the best matching FAQ.

```text
POST /chat

```

**Request Body (JSON):**

```json
{
  "question": "How do I start using the chatbot?"
}

```

**Response (JSON):**

```json
{
  "answer": "You can start by typing your question in the chat box and pressing Enter...",
  "confidence": 0.85,
  "matched_question": "How do I start using the chatbot?"
}

```

---

## Usage

1. **Initiate Chat:** Type your question into the input field at the bottom of the interface.
2. **Submit:** Press the **Send** button or hit the **Enter** key.
3. **Review Response:** The bot will display the most relevant answer from its database.
4. **Confidence Level:** Check the small text below the input field to see how accurate the bot believes its answer is.