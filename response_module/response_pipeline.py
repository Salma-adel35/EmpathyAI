"""
Main pipeline interface for the EmpathyAI Response Generation module.
Exposes process_response for backend integration.
"""

from response_module.prompt_templates import format_prompt
from response_module.llm_client import call_llm
from response_module.safety import check_response_safety
from response_module.fallbacks import generate_safe_fallback

def generate_response(
    message: str,
    emotion: dict,
    intent: dict,
    conversation_memory: list,
    retrieved_knowledge: list
) -> str:
    """Constructs prompt, sends to LLM, or uses fallback if unavailable."""
    system_prompt, user_prompt = format_prompt(
        message, emotion, intent, conversation_memory, retrieved_knowledge
    )

    llm_output = call_llm(system_prompt, user_prompt)

    if llm_output:
        return llm_output
    
    return generate_safe_fallback(message, emotion, intent)


def process_response(
    message: str,
    emotion: dict,
    intent: dict,
    conversation_memory: list = None,
    retrieved_knowledge: list = None
) -> dict:
    """
    REQUIRED CONTRACT FUNCTION FOR BACKEND INTEGRATION.
    
    Input:
        message (str)
        emotion (dict) -> {"label": "anxiety", "confidence": 0.91}
        intent (dict) -> {"label": "seeking_support", "confidence": 0.94}
        conversation_memory (list)
        retrieved_knowledge (list)
        
    Output:
        {
            "response": "...",
            "safety_status": "safe" | "fallback"
        }
    """
    if conversation_memory is None:
        conversation_memory = []
    if retrieved_knowledge is None:
        retrieved_knowledge = []

    # 1. Generate response via LLM (or fallback)
    raw_response = generate_response(
        message, emotion, intent, conversation_memory, retrieved_knowledge
    )

    # 2. Safety Check
    safety_result = check_response_safety(raw_response)

    # 3. Return safe response or fallback
    if safety_result["is_safe"]:
        return {
            "response": raw_response,
            "safety_status": "safe"
        }
    else:
        safe_response = generate_safe_fallback(message, emotion, intent)
        return {
            "response": safe_response,
            "safety_status": "fallback"
        }