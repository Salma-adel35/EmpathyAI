from typing import Dict, Any


def build_full_context(
    message: str,
    emotion_result: Dict[str, Any],
    intent_result: Dict[str, Any],
    context_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Combine outputs from all analysis modules
    into one unified context object.

    This function does not run emotion or intent models.
    It only combines their outputs.
    """

    return {
        "message": message,

        "emotion": emotion_result.get(
            "emotion",
            {}
        ),

        "screening": emotion_result.get(
            "screening",
            {}
        ),

        "risk_level": emotion_result.get(
            "risk_level",
            "low"
        ),

        "intent": intent_result.get(
            "intent",
            "unknown"
        ),

        "intent_confidence": intent_result.get(
            "confidence",
            0.0
        ),

        "conversation_memory": context_result.get(
            "conversation_memory",
            []
        ),

        "retrieved_knowledge": context_result.get(
            "retrieved_knowledge",
            []
        )
    }