# EmpathyAI Context Module

The Context Module is responsible for providing contextual information to the response generation pipeline.

It combines two main components:

1. **Short-term Conversation Memory** using SQLite.
2. **Retrieval-Augmented Generation (RAG)** using Sentence Transformers and FAISS.

The output of this module helps the response generator produce responses that are aware of both the previous conversation and relevant knowledge from the local knowledge base.

---

# Project Structure

```text
context_module/
│
├── __init__.py
├── memory.py
├── database.py
├── rag.py
├── context_manager.py
│
├── knowledge_base/
│   ├── stress_management.txt
│   ├── anxiety_support.txt
│   ├── emotional_support.txt
│   └── study_stress.txt
│
├── memory.db
├── requirements.txt
└── README.md
```

---

# Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Conversation Memory

The memory module stores recent conversation messages for each user using a local SQLite database.

Each message contains:

- User ID
- Role (`user` or `assistant`)
- Message content
- Timestamp

---

## Add a Message

```python
from context_module.memory import add_message

add_message(
    user_id="user_1",
    role="user",
    content="I have an exam tomorrow."
)
```

Supported roles:

- `user`
- `assistant`

---

## Retrieve Conversation Context

```python
from context_module.memory import get_conversation_context

context = get_conversation_context(
    user_id="user_1",
    max_messages=6
)
```

Example output:

```python
[
    {
        "role": "user",
        "content": "I have an exam tomorrow."
    },
    {
        "role": "assistant",
        "content": "That sounds stressful."
    }
]
```

Only the most recent messages (default = 6) are returned to keep the prompt concise.

---

## Clear Conversation Memory

```python
from context_module.memory import clear_memory

clear_memory("user_1")
```

---

# Retrieval-Augmented Generation (RAG)

The RAG module retrieves relevant supportive information from a local knowledge base.

It uses:

- Sentence Transformers
- `all-MiniLM-L6-v2` embedding model
- FAISS vector search

The knowledge base currently includes information about:

- Stress management
- Anxiety support
- Emotional support
- Study stress

---

## Building the Vector Index

When the module starts:

1. All text files are loaded from the `knowledge_base` folder.
2. Each document is converted into an embedding using `all-MiniLM-L6-v2`.
3. The embeddings are stored inside a FAISS `IndexFlatL2` index.
4. The index remains in memory for fast retrieval during runtime.

---

## Retrieve Relevant Knowledge

```python
from context_module.rag import retrieve_relevant_context

results = retrieve_relevant_context(
    query="I feel stressed about my exam.",
    top_k=3
)
```

Example output:

```python
[
    {
        "text": "Studying for an important exam can create pressure...",
        "score": 0.92
    }
]
```

---

## Similarity Metric

The current FAISS implementation uses **L2 (Euclidean) Distance**.

Therefore:

```text
Lower distance = More relevant result
```

The returned score represents the distance between the user's query embedding and the stored document embedding.

---

# Unified Context Interface

The Context Manager combines conversation memory and retrieved knowledge into one unified object.

```python
from context_module.context_manager import get_context

context = get_context(
    user_id="user_1",
    query="I feel stressed about my exam."
)
```

Example output:

```python
{
    "conversation_memory": [
        {
            "role": "user",
            "content": "I have an exam tomorrow."
        }
    ],

    "retrieved_knowledge": [
        {
            "text": "...",
            "score": 0.92
        }
    ]
}
```

---

# Integration with the Main Backend

The backend retrieves contextual information before generating a response.

```python
from context_module.context_manager import get_context

context = get_context(
    user_id=user_id,
    query=user_message
)
```

The resulting context is then passed to the response generation module.

```python
response = process_response(
    message=user_message,
    emotion=emotion_result,
    intent=intent_result,
    conversation_memory=context["conversation_memory"],
    retrieved_knowledge=context["retrieved_knowledge"]
)
```

---

# Design Decisions

### Why SQLite?

SQLite was chosen because it:

- Is lightweight
- Requires no server setup
- Persists conversation history between application restarts
- Is suitable for a prototype application

---

### Why FAISS?

FAISS enables efficient nearest-neighbor search over vector embeddings, making retrieval significantly faster than scanning all documents sequentially.

---

### Why Sentence Transformers?

The `all-MiniLM-L6-v2` model generates compact semantic embeddings, allowing the system to retrieve documents based on meaning rather than exact keyword matching.

---

# Safety Notes

The retrieved knowledge is intended to provide general emotional support and educational information.

The system does **not**:

- Diagnose mental or physical health conditions
- Provide personalized medical advice
- Prescribe medications
- Replace professional mental health care

---

# Current Limitations

- The knowledge base is currently static and consists of local text files.
- The FAISS index is rebuilt when the application starts.
- Conversation history is stored locally using SQLite and is not synchronized across multiple devices.
- The current implementation is designed for a prototype and can later be extended with larger databases and cloud storage.

---

# Summary

The Context Module provides the response generation pipeline with:

- Recent conversation history
- Relevant retrieved knowledge
- Fast semantic search using FAISS
- Persistent local conversation memory using SQLite

Together, these components enable EmpathyAI to generate responses that are more context-aware, coherent, and relevant to the user's current situation.
