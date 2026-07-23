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

    system_prompt, user_prompt = format_prompt(
        message=message,
        emotion=emotion,
        intent=intent,
        conversation_memory=conversation_memory,
        retrieved_knowledge=retrieved_knowledge
    )

    print("SYSTEM PROMPT:")
    print(system_prompt)

    print("USER PROMPT:")
    print(user_prompt)

    print("MEMORY SENT TO RESPONSE:")
    print(conversation_memory)

    print("RAG KNOWLEDGE SENT TO RESPONSE:")
    print(retrieved_knowledge)

    llm_output = call_llm(
        system_prompt,
        user_prompt
    )

    if llm_output:
        return llm_output

    return generate_safe_fallback(
        message,
        emotion,
        intent
    )


def process_response(
    message: str,
    emotion: dict,
    intent: dict,
    conversation_memory: list = None,
    retrieved_knowledge: list = None
) -> dict:

    if conversation_memory is None:
        conversation_memory = []

    if retrieved_knowledge is None:
        retrieved_knowledge = []

    raw_response = generate_response(
        message=message,
        emotion=emotion,
        intent=intent,
        conversation_memory=conversation_memory,
        retrieved_knowledge=retrieved_knowledge
    )

    safety_result = check_response_safety(
        raw_response
    )

    if safety_result.get("is_safe", False):

        return {
            "response": raw_response,
            "safety_status": "safe"
        }

    safe_response = generate_safe_fallback(
        message,
        emotion,
        intent
    )

    return {
        "response": safe_response,
        "safety_status": "fallback"
    }