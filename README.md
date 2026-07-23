# EmpathyAI

### An Emotion-Aware Conversational AI for Supportive and Context-Aware Conversations

EmpathyAI is an intelligent conversational AI system designed to provide empathetic, context-aware emotional support through natural language interaction.

The system combines **emotion recognition, intent classification, conversational memory, Retrieval-Augmented Generation (RAG), safety validation, and Large Language Model (LLM) integration** to generate responses that are more relevant, personalized, and emotionally aware.

---

## Overview

Traditional conversational systems often respond only to the current user message. EmpathyAI takes a broader approach by analyzing the user's emotional state, understanding their conversational intent, retrieving relevant knowledge, and considering previous conversation context before generating a response.

The system follows this pipeline:

```text
User Message
     │
     ▼
Emotion Detection
     │
     ▼
Intent Classification
     │
     ▼
Conversation Memory ─────┐
                         │
                         ▼
                    RAG Retrieval
                         │
                         ▼
                  Response Generation
                         │
                         ▼
                    Safety Checking
                         │
                         ▼
                   Final Response
```

---

## Key Features

### Emotion Detection

EmpathyAI analyzes the emotional state expressed in the user's message using a trained deep learning model.

The emotion module is responsible for:

* Emotion classification
* Emotion probability estimation
* Text preprocessing
* Emotional context extraction

The detected emotion is used to help the response generation system adapt its tone.

---

### Intent Classification

A fine-tuned Transformer-based intent classification model identifies the user's conversational goal.

Supported intents include:

* `venting`
* `seeking_support`
* `seeking_advice`
* `seeking_motivation`
* `casual_conversation`

The detected intent determines how the system should respond.

For example:

| Intent              | Response Behavior                                     |
| ------------------- | ----------------------------------------------------- |
| Venting             | Listen and validate without immediately giving advice |
| Seeking Support     | Provide emotional reassurance                         |
| Seeking Advice      | Provide practical and concise suggestions             |
| Seeking Motivation  | Encourage and acknowledge effort                      |
| Casual Conversation | Respond naturally and conversationally                |

---

### Context-Aware Conversation Memory

EmpathyAI maintains relevant conversation history to support continuity across multiple messages.

This allows the system to understand references such as:

> "I still feel stressed about the exam I told you about."

Instead of treating the message as an isolated input, the system can use relevant previous context to generate a more coherent response.

Conversation memory is managed through the context module and persistent storage.

---

### Retrieval-Augmented Generation (RAG)

The system retrieves relevant knowledge based on the user's current message.

Retrieved information can include general supportive knowledge related to:

* Stress
* Anxiety
* Emotional support
* Exam pressure
* Time management
* Coping with overwhelming responsibilities

The retrieved context is passed to the response generation layer only when it is relevant to the current conversation.

---

### LLM-Powered Response Generation

EmpathyAI uses a Large Language Model to generate natural language responses based on:

* The current user message
* Detected emotion
* Detected intent
* Relevant conversation memory
* Retrieved knowledge

The system uses structured prompt engineering to ensure that generated responses are:

* Empathetic
* Context-aware
* Concise
* Natural
* Non-judgmental

The response generation layer also includes fallback responses in case the external LLM API is unavailable.

---

### Safety Layer

Generated responses pass through a safety validation layer before being returned to the user.

The system is designed to:

* Avoid medical diagnoses
* Avoid prescribing medication
* Avoid pretending to be human
* Avoid judgmental or harmful responses
* Provide safer fallback responses when needed

---

### Multi-Component Architecture

EmpathyAI is organized into modular components:

```text
EmpathyAI/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   └── services/
│
├── emotion_module/
│   ├── emotion_model.py
│   ├── screening_model.py
│   ├── preprocessing.py
│   └── predict.py
│
├── intent_module/
│   ├── intent_inference.py
│   ├── tokenizer.json
│   └── model files
│
├── context_module/
│   ├── memory.py
│   ├── rag.py
│   └── database.py
│
├── response_module/
│   ├── llm_client.py
│   ├── prompt_builder.py
│   ├── prompt_templates.py
│   ├── response_pipeline.py
│   ├── safety_checker.py
│   └── fallbacks.py
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── components/
│   ├── assets/
│   └── utils/
│
└── tests/
```

---

## Technology Stack

### Programming Language

* Python

### Machine Learning & NLP

* PyTorch
* Hugging Face Transformers
* BERT-based models
* Natural Language Processing

### LLM Integration

* Google Gemini API

### Backend

* Flask
* REST API

### Frontend

* Streamlit

### Context & Retrieval

* Retrieval-Augmented Generation (RAG)
* Vector similarity search
* Conversation memory
* SQLite-based persistence

### Development Tools

* Git
* GitHub
* Virtual Environments

---

## API Workflow

The main conversation endpoint receives a user message:

```http
POST /chat
```

Example request:

```json
{
  "user_id": "user_1",
  "message": "I feel overwhelmed because I have too many responsibilities."
}
```

The backend processes the message through the complete pipeline:

```text
User Input
    ↓
Emotion Analysis
    ↓
Intent Detection
    ↓
Memory Retrieval
    ↓
Knowledge Retrieval
    ↓
LLM Response Generation
    ↓
Safety Validation
    ↓
Final API Response
```

Example response:

```json
{
  "response": "Generated empathetic response",
  "safety_status": "safe",
  "intent_analysis": {
    "label": "seeking_advice",
    "confidence": 0.71
  },
  "retrieved_knowledge": []
}
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Salma-adel35/EmpathyAI.git
cd EmpathyAI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r backend/requirements.txt
```

For the response generation module:

```bash
pip install -r response_module/requirements.txt
```

---

## Environment Variables

Create a `.env` file and add your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit API keys or other secrets to the repository.

---

## Running the Backend

From the project root:

```bash
python -m backend.app
```

The backend API will be available at:

```text
http://127.0.0.1:5000
```

---

## Running the Frontend

In a separate terminal:

```bash
streamlit run frontend/app.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

---

## Testing the API

Example using PowerShell:

```powershell
$response = Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_id":"user_1","message":"I feel stressed about my upcoming exam"}'

$response.response
```

---

## Example Conversations

### Seeking Support

**User:**

> I feel really lonely today and I just need someone to support me.

**EmpathyAI:**

> The loneliness you're feeling can make the day feel especially heavy. Reaching out when you need support is meaningful, and you don't have to explain everything perfectly to be heard.

---

### Seeking Advice

**User:**

> I have been procrastinating a lot lately. What can I do to manage my time better?

**EmpathyAI:**

> When everything feels overwhelming, try choosing one small task and working on it for just a few minutes instead of focusing on everything at once. Breaking a large task into smaller steps can make it easier to get started.

---

### Context-Aware Conversation

**User:**

> I have an important exam next week and I am very stressed about it.

**Assistant:**

> Exam pressure can feel heavy, especially when an important deadline is approaching.

**User:**

> I still feel stressed about the exam I told you about.

**Assistant:**

> The system uses the previous conversation context to understand what "the exam I told you about" refers to and generate a context-aware response.

---

## Project Goals

EmpathyAI was designed to explore the integration of multiple AI components into a complete end-to-end application.

The project demonstrates how:

* Machine Learning models can work together in a single pipeline
* Emotion recognition can improve conversational responses
* Intent classification can control response behavior
* RAG can provide relevant contextual knowledge
* Conversation memory can preserve context across messages
* LLMs can generate natural language responses
* Safety layers can improve response reliability

---

## Future Improvements

Potential future improvements include:

* Multilingual emotion and intent classification
* Improved Arabic language support
* More advanced long-term memory
* Better retrieval ranking
* Streaming responses
* Voice-based interaction
* More extensive evaluation metrics
* Model hosting through Hugging Face Hub
* Production deployment with Docker

---

## Disclaimer

EmpathyAI is an AI research and software project designed to provide supportive conversational interactions.

It is not a replacement for professional medical or mental health care and should not be used for diagnosis, treatment, or emergency assistance.

---

## Author

**Salma Adel**

Computer Engineering Student | AI & Machine Learning Enthusiast

GitHub: [Salma-adel35](https://github.com/Salma-adel35)

---

## License

This project is intended for educational and research purposes.
