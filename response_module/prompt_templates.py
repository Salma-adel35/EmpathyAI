"""
Prompt engineering templates for EmpathyAI response generation.
"""

SYSTEM_PROMPT = """You are EmpathyAI, a supportive, empathetic conversational AI assistant.

Your primary goal is to listen, validate feelings, and offer grounded emotional support.

STRICT INSTRUCTIONS:
1. ACKNOWLEDGE & VALIDATE: Explicitly validate the user's emotional state without exaggerating.
2. ADAPT TO DETECTED INTENT:
   - venting: Listen attentively, validate feelings, do NOT offer unprompted advice or solutions.
   - seeking_support: Offer comfort, empathy, reassurance, and steady presence.
   - seeking_advice: Offer 1-2 small, practical, non-intrusive suggestions after validating feelings.
   - seeking_motivation: Offer encouragement, highlight their efforts, and boost confidence.
   - casual_conversation: Keep the tone light, friendly, and natural.
3. CONTEXT & KNOWLEDGE: Use conversation memory and retrieved knowledge ONLY if directly relevant. Do not dump raw facts.
4. TONE & BOUNDARIES:
   - Keep responses concise (2 to 4 sentences).
   - Be natural, empathetic, and direct.
   - NEVER pretend to be a human or have physical experiences.
   - NEVER diagnose mental or physical health conditions.
   - NEVER prescribe medical treatments or medications.
   - NEVER be preachy, judgmental, or overly clinical.
"""

USER_PROMPT_TEMPLATE = """
USER MESSAGE:
"{message}"

DETECTED EMOTION: {emotion_label} (Confidence: {emotion_confidence})
DETECTED INTENT: {intent_label} (Confidence: {intent_confidence})

CONVERSATION MEMORY:
{formatted_memory}

RETRIEVED KNOWLEDGE (RAG):
{formatted_knowledge}

Please generate an empathetic, concise, and context-aware response following your system instructions.
"""

def format_prompt(
    message: str,
    emotion: dict,
    intent: dict,
    conversation_memory: list,
    retrieved_knowledge: list
) -> tuple[str, str]:
    """Formats system and user prompts with dynamic values."""
    
    # Safely extract labels and confidences
    emotion_label = emotion.get("label", "neutral") if isinstance(emotion, dict) else "neutral"
    emotion_conf = emotion.get("confidence", 1.0) if isinstance(emotion, dict) else 1.0
    intent_label = intent.get("label", "casual_conversation") if isinstance(intent, dict) else "casual_conversation"
    intent_conf = intent.get("confidence", 1.0) if isinstance(intent, dict) else 1.0

    # Format memory list
    if conversation_memory and isinstance(conversation_memory, list):
        mem_str = "\n".join(
            [f"- {msg.get('role', 'user')}: {msg.get('content', '')}" for msg in conversation_memory if isinstance(msg, dict)]
        )
    else:
        mem_str = "None"

    # Format retrieved knowledge list
    if retrieved_knowledge and isinstance(retrieved_knowledge, list):
        know_str = "\n".join(
            [f"- {item.get('text', '')}" for item in retrieved_knowledge if isinstance(item, dict)]
        )
    else:
        know_str = "None"

    user_content = USER_PROMPT_TEMPLATE.format(
        message=message,
        emotion_label=emotion_label,
        emotion_confidence=emotion_conf,
        intent_label=intent_label,
        intent_confidence=intent_conf,
        formatted_memory=mem_str,
        formatted_knowledge=know_str
    )

    return SYSTEM_PROMPT, user_content