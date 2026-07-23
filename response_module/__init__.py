"""
response_module
===============
EmpathyAI — Response Generation & Safety Module 

Public API
----------
>>> from response_module.response_generator import generate_response
>>> result = generate_response(message, emotion, intent, screening, context)
>>> # result → {"response": str, "safety_status": "safe" | "flagged"}
"""

from .response_generator import generate_response  # noqa: F401

__all__ = ["generate_response"]
__version__ = "1.0.0"
