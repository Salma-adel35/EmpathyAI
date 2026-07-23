"""
Safe fallback generator when API is unavailable or response fails safety checks.
"""

FALLBACK_TEMPLATES = {
    # =========================
    # ANXIETY
    # =========================

    ("anxiety", "seeking_support"): (
        "It sounds like your mind is carrying a lot of worry right now. "
        "You do not have to figure everything out at once—take a moment to slow down and focus on what feels most important right now."
    ),

    ("anxiety", "venting"): (
        "That sounds really difficult to sit with. "
        "You can take your time and tell me what has been making you feel this anxious."
    ),

    ("anxiety", "seeking_advice"): (
        "When anxiety makes everything feel overwhelming, try focusing on one small, specific task instead of the whole situation at once. "
        "A short pause and a simple next step can make things feel a little more manageable."
    ),

    ("anxiety", "seeking_motivation"): (
        "Feeling nervous does not mean you are incapable of handling this. "
        "Focus on the next small step you can take, rather than expecting yourself to have everything figured out immediately."
    ),

    # =========================
    # SADNESS
    # =========================

    ("sadness", "venting"): (
        "That sounds like a painful feeling to carry. "
        "You do not need to force yourself to feel better right now—if you want to talk about what happened, I am listening."
    ),

    ("sadness", "seeking_support"): (
        "It sounds like today has been emotionally difficult for you. "
        "You deserve some patience and support while you are going through this."
    ),

    ("sadness", "seeking_advice"): (
        "When everything feels heavy, try focusing on one small thing that could make the next hour a little easier. "
        "You do not need to solve everything today."
    ),

    ("sadness", "seeking_motivation"): (
        "The fact that you are still trying despite feeling this way says something about your strength. "
        "You can take things slowly and focus only on the next step."
    ),

    # =========================
    # STRESS
    # =========================

    ("stress", "seeking_advice"): (
        "Having many things to handle at once can make it difficult to know where to begin. "
        "Try choosing one priority and breaking it into the smallest possible first step before moving on to anything else."
    ),

    ("stress", "seeking_support"): (
        "It sounds like you have been under a lot of pressure lately. "
        "You do not have to carry every responsibility mentally all at once."
    ),

    ("stress", "venting"): (
        "That sounds like a lot to deal with at the same time. "
        "You can let it out here and tell me what has been weighing on you the most."
    ),

    ("stress", "seeking_motivation"): (
        "You have already been putting effort into dealing with a lot. "
        "You do not need to finish everything at once—one manageable step is enough to start."
    ),

    # =========================
    # ANGER
    # =========================

    ("anger", "venting"): (
        "It sounds like something has really pushed you to your limit. "
        "You can tell me what happened and get it off your chest."
    ),

    ("anger", "seeking_support"): (
        "That sounds frustrating and emotionally exhausting. "
        "You deserve a moment to process what happened before trying to deal with everything else."
    ),

    ("anger", "seeking_advice"): (
        "When frustration is running high, it can help to pause before deciding what to do next. "
        "Then try focusing on the specific part of the situation that you can actually control."
    ),

    # =========================
    # HAPPINESS
    # =========================

    ("happiness", "casual_conversation"): (
        "That sounds great! "
        "I am glad something positive happened—tell me more about it if you would like."
    ),

    ("happiness", "seeking_support"): (
        "It is nice to hear that you are feeling good about this. "
        "You deserve to enjoy the positive moments when they come."
    ),

    # =========================
    # NEUTRAL
    # =========================

    ("neutral", "casual_conversation"): (
        "I am listening. "
        "Tell me a little more about what is on your mind."
    ),

    ("neutral", "seeking_support"): (
        "It sounds like you could use some support with what you are dealing with right now. "
        "You can start by telling me whatever feels most important."
    ),

    ("neutral", "seeking_advice"): (
        "Let's break the situation down into one manageable next step. "
        "Starting small can make it easier to decide what to do next."
    ),

    ("neutral", "venting"): (
        "Go ahead and let it out. "
        "I am listening to what has been bothering you."
    )
}


def generate_safe_fallback(
    message: str,
    emotion: dict,
    intent: dict
) -> str:
    """
    Generates a contextual and safe fallback response.

    The response is selected based on the detected emotion and intent.
    """

    e_label = (
        emotion.get("label", "neutral")
        if isinstance(emotion, dict)
        else "neutral"
    )

    i_label = (
        intent.get("label", "casual_conversation")
        if isinstance(intent, dict)
        else "casual_conversation"
    )

    key = (e_label, i_label)

    # Exact emotion + intent match
    if key in FALLBACK_TEMPLATES:
        return FALLBACK_TEMPLATES[key]

    # If exact combination is unavailable,
    # prioritize the detected intent.
    intent_fallbacks = {
        "venting": (
            "It sounds like you have a lot on your mind right now. "
            "You can take your time and tell me what has been weighing on you."
        ),

        "seeking_support": (
            "It sounds like you are going through something difficult right now. "
            "You do not have to explain everything perfectly—start wherever feels easiest."
        ),

        "seeking_advice": (
            "It sounds like there is a lot to deal with right now. "
            "Try focusing on one small, manageable step instead of trying to solve everything at once."
        ),

        "seeking_motivation": (
            "You have already taken a step by continuing to try. "
            "Focus on what you can do next, one manageable step at a time."
        ),

        "casual_conversation": (
            "I am listening. "
            "Tell me a little more about what is on your mind."
        )
    }

    return intent_fallbacks.get(
        i_label,
        "It sounds like you have a lot on your mind right now. "
        "Tell me a little more about what you are going through."
    )