# Language Translation Tool

A professional full-stack web application designed for real-time multilingual text translation. This project utilizes a Python Flask backend to interface with translation engines and a modern JavaScript-driven frontend for a seamless user experience.

---

## Table of Contents
* [Features](#features)
* [Technical Stack](#technical-stack)
* [Project Structure](#project-structure)
* [Installation and Setup](#installation-and-setup)
* [API Documentation](#api-documentation)
* [Usage](#usage)

---

## Features
* **Real-time Translation:** Synchronous text processing across multiple global languages.
* **Integrated Text-to-Speech:** Native browser support for reading translations aloud using the `SpeechSynthesisUtterance` interface.
* **Clipboard Management:** One-click functionality to copy translated text to the system clipboard.
* **Responsive Interface:** A clean, centered layout featuring custom CSS animations and a loading spinner for better UX.
* **Health Monitoring:** Dedicated endpoints to verify API status and check server health.

---

## Technical Stack

### Backend
* **Python/Flask:** Core API framework.
* **Flask-CORS:** Manages cross-origin resource sharing for secure frontend-to-backend communication.
* **Deep-Translator:** Interfaces with Google Translate engine.

### Frontend
* **HTML5:** Semantic structure including a localized language selector and accessible text areas.
* **CSS3:** Custom styling utilizing Flexbox for a responsive, centered container.
* **JavaScript (ES6+):** Uses Fetch API for asynchronous POST requests to the Flask server.

---

## Project Structure
```

Language-Translation-Tool/
│
├── app.py          
├── requirements.txt
├── index.html     
├── style.css       
├── script.js       
└── README.md      

````

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
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000` by default. Open `index.html` in your browser to access the UI.

---

## API Documentation

### Health Check

```
GET /api/health
```

**Response:**

```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### Translation Endpoint

```
POST /api/translate
```

**Request Body (JSON):**

```json
{
  "source_language": "en",
  "target_language": "es",
  "text": "Hello, how are you?"
}
```

**Response:**

```json
{
  "translated_text": "Hola, ¿cómo estás?"
}
```

---

## Usage

1. Select the **source** and **target** languages from the dropdown menus.
2. Enter text in the **source** text area.
3. Click **Translate** to get the translated text.
5. Use the **Copy** button to save translated text to the clipboard.

---