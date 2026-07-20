"""
Safe fallback generator when API is unavailable or response fails safety checks.
"""

FALLBACK_TEMPLATES = {
    ("anxiety", "seeking_support"): (
        "It is completely understandable to feel anxious right now. Please take a deep, slow breath—you "
        "have put in a lot of effort, and taking things one step at a time is all you need to do right now."
    ),
    ("sadness", "venting"): (
        "I hear you, and it is completely valid to feel down. I'm here to listen whenever you want to express "
        "what is on your mind."
    ),
    ("stress", "seeking_advice"): (
        "When stress starts building up, breaking tasks down into small, manageable steps can help. "
        "Consider taking a brief 5-minute break to clear your head before tackling the next piece."
    ),
    ("happiness", "casual_conversation"): (
        "That sounds wonderful! I am really glad to hear things are going well for you."
    ),
    ("anxiety", "seeking_motivation"): (
        "Nervousness often comes when you care deeply about what you are doing. Trust the preparation you've "
        "done—you are far more capable than you give yourself credit for!"
    )
}

DEFAULT_FALLBACK = (
    "I hear you, and I am here to support you. Let's take things one moment at a time."
)

def generate_safe_fallback(message: str, emotion: dict, intent: dict) -> str:
    """Generates a contextual, safe fallback message."""
    e_label = emotion.get("label", "neutral") if isinstance(emotion, dict) else "neutral"
    i_label = intent.get("label", "casual_conversation") if isinstance(intent, dict) else "casual_conversation"

    key = (e_label, i_label)
    return FALLBACK_TEMPLATES.get(key, DEFAULT_FALLBACK)