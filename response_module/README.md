# EmpathyAI — Response Module 

Handles **response generation** and **safety checking** for the EmpathyAI pipeline.

## Directory Structure

```
response_module/
├── __init__.py           # Package init — exposes generate_response()
├── llm_client.py         # OpenAI API wrapper (key loaded from .env)
├── prompt_builder.py     # Builds system + user prompts from all upstream inputs
├── safety_checker.py     # Rule-based safety filter (regex + keyword patterns)
├── response_generator.py # Main pipeline entry point with fallback logic
└── requirements.txt      # Python dependencies
tests/
└── test_response.py      # Full pytest test suite (37 tests)
```

## Setup

```bash
# 1. Install dependencies
pip install -r response_module/requirements.txt

# 2. Create .env in the project root (NEVER commit this file)
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Optional model overrides
echo "EMPATHY_MODEL=gpt-4o"       >> .env
echo "EMPATHY_MAX_TOKENS=256"     >> .env
echo "EMPATHY_TEMPERATURE=0.7"    >> .env
echo "EMPATHY_TIMEOUT=15"         >> .env
```

## Usage

```python
from response_module.response_generator import generate_response

result = generate_response(
    message   = "I am feeling overwhelmed by my exam tomorrow.",
    emotion   = {"label": "stress", "confidence": 0.91},
    intent    = {"intent": "seeking_support", "confidence": 0.89},
    screening = {"indicator": "anxiety_related", "confidence": 0.78, "risk_level": "low"},
    context   = {
        "conversation_memory": [
            {"role": "user", "content": "I have been studying for hours."}
        ],
        "retrieved_knowledge": [
            {"text": "Deep breathing reduces study stress.", "score": 0.85}
        ]
    }
)

print(result)
# {"response": "...", "safety_status": "safe"}
```

## Pipeline Overview

```
generate_response()
       │
       ▼
build_messages()          ← prompt_builder.py
       │                    (weaves emotion + intent + screening + context)
       ▼
call_llm()                ← llm_client.py
       │
       ├── None returned? → _get_fallback()   [zero-downtime guarantee]
       │
       ▼
check_safety()            ← safety_checker.py
       │
       ├── Flagged?       → _get_fallback()   [safety guarantee]
       │
       ▼
{"response": ..., "safety_status": "safe" | "flagged"}
```

## Fallback Guarantee

If `OPENAI_API_KEY` is missing **or** the LLM call fails for **any** reason,
`generate_response()` returns a pre-written, emotion- and risk-aware fallback
response with `safety_status: "safe"` — guaranteeing **zero downtime** for the
backend regardless of external API availability.

## Safety Checker

Three violation categories are checked via regex before any response reaches
the user:

| Category | Examples caught |
|----------|----------------|
| **Diagnostic** | "you have depression", "sounds like OCD" |
| **Prescription** | "take sertraline", "try Xanax" |
| **Harmful** | "get over it", "man up", "you're weak" |

## Running Tests

```bash
pytest tests/test_response.py -v
```

Expected output: **37 tests passing**, no API key required (all LLM calls
are mocked).
