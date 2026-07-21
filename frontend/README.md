# EmpathyAI Frontend

The frontend interface for EmpathyAI, an emotionally-aware conversational AI assistant.

## Features

- ChatGPT-style conversational interface
- Emotion-aware interaction
- Emotional journey visualization
- Conversation context indicators
- Suggested conversation starters
- Backend API integration support
- Mock API mode for local development

## Tech Stack

- Python
- Streamlit
- Requests
- python-dotenv

## Run Locally

From the frontend directory:

```bash
pip install -r requirements.txt
````

Create a `.env` file:

```env
BACKEND_URL=http://localhost:5000
USE_MOCK_API=true
```

Run:

```bash
streamlit run app.py
```

## Backend Integration

After the backend is deployed, update:

```env
USE_MOCK_API=false
BACKEND_URL=YOUR_BACKEND_URL
```

The frontend will then send requests to:

```text
POST /chat
```

Expected request:

```json
{
  "user_id": "user_001",
  "message": "I feel overwhelmed"
}
```

Expected response:

```json
{
  "response": "It sounds like you are feeling overwhelmed...",
  "emotion": "Stress",
  "emotion_emoji": "😣",
  "intent": "seeking_support",
  "memory_used": true,
  "rag_used": true,
  "safety_status": "safe"
}
