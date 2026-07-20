"""
EmpathyAI — Response Generation & Safety Module
"""

from response_module.response_pipeline import process_response, generate_response
from response_module.safety import check_response_safety
from response_module.fallbacks import generate_safe_fallback

__all__ = [
    "process_response",
    "generate_response",
    "check_response_safety",
    "generate_safe_fallback"
]