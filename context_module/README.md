# EmpathyAI Context Module

This module provides two main capabilities:

1. Short-term conversation memory.
2. Retrieval-Augmented Generation (RAG).

The module combines recent conversation history with relevant knowledge from a local knowledge base.

---

## Project Structure

```text
context_module/
│
├── __init__.py
├── memory.py
├── rag.py
├── context_manager.py
│
├── knowledge_base/
│   ├── stress_management.txt
│   ├── anxiety_support.txt
│   ├── emotional_support.txt
│   └── study_stress.txt
│
├── requirements.txt
└── README.md
````

---

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Conversation Memory

The memory module stores recent messages for each user.

## Add a message

```python
from context_module.memory import add_message

add_message(
    user_id="user_1",
    role="user",
    content="I have an exam tomorrow."
)
```

The supported roles are:

* `user`
* `assistant`

---

## Retrieve conversation context

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

---

## Clear memory

```python
from context_module.memory import clear_memory

clear_memory("user_1")
```

---

# RAG

The RAG module uses:

* `sentence-transformers`
* `all-MiniLM-L6-v2`
* `FAISS`

The knowledge base contains information related to:

* Stress management
* Anxiety support
* Emotional support
* Study stress

---

## Retrieve relevant knowledge

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

### Important

The current FAISS index uses L2 distance.

Therefore:

```text
Lower distance = More relevant result
```

---

# Unified Context Interface

The main function combines memory and RAG:

```python
from context_module.context_manager import get_context

context = get_context(
    user_id="user_1",
    query="I feel stressed about my exam."
)
```

Output:

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

# Integration With the Main Backend

The backend can use:

```python
from context_module.context_manager import get_context

context = get_context(
    user_id=user_id,
    query=user_message
)
```

Then pass the result to the Response Generation module:

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

# Safety Note

The knowledge base provides general supportive information.

It does not provide:

* Medical diagnosis
* Personalized medical treatment
* Medication prescriptions

---

# Limitations

The current memory implementation stores data in memory and is intended for the prototype version.

Conversation data will be lost when the application restarts.

For a production system, the memory can later be replaced with a database or persistent storage solution.

