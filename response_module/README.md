# EmpathyAI — Response Generation & Safety Module

This module handles prompt engineering, response generation using LLMs (or safe contextual fallbacks), and automated safety guardrails for the **EmpathyAI** pipeline.

## 🚀 Quick Start

Import `process_response` directly in the main backend pipeline:

```python
from response_module.response_pipeline import process_response

result = process_response(
    message="I studied all day but I still feel like I am going to fail.",
    emotion={"label": "anxiety", "confidence": 0.91},
    intent={"label": "seeking_support", "confidence": 0.94},
    conversation_memory=[],
    retrieved_knowledge=[]
)

print(result)
# Output:
# {
#     "response": "It sounds like you have been working really hard, and it is understandable to feel anxious about the result.",
#     "safety_status": "safe"
# }