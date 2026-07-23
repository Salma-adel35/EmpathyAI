"""
response_generator.py
=====================
Main public entry point for the EmpathyAI response pipeline.

Pipeline order
--------------
1. Build structured LLM messages from all upstream contract inputs.
2. Call the LLM via llm_client.call_llm().
3. If LLM returns None (key missing / API error) → emotion-aware fallback.
4. Run safety_checker.check_safety() on the LLM output.
5. If flagged → replace with a risk-sensitive safe fallback.
6. Return {"response": str, "safety_status": "safe" | "flagged"}.
"""

import logging
from typing import Any

from .llm_client     import call_llm
from .prompt_builder import build_messages
from .safety_checker import check_safety

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Pre-vetted fallback responses
# Priority: risk_level (high/moderate) > emotion label > generic default.
# ─────────────────────────────────────────────────────────────────────────────

_FALLBACKS_BY_RISK: dict[str, str] = {
    "high": (
        "I can hear that you're going through something really difficult right now, "
        "and I want you to know you're not alone. "
        "Please consider reaching out to a crisis helpline or a mental-health "
        "professional who can give you the support you deserve — "
        "your well-being matters deeply."
    ),
    "moderate": (
        "It sounds like things feel quite heavy for you right now, "
        "and that's completely valid. "
        "Talking to a counsellor or a trusted person in your life can make "
        "a real difference — you don't have to face this alone."
    ),
}

_FALLBACKS_BY_EMOTION: dict[str, str] = {
    "stress": (
        "It's completely understandable to feel stressed — "
        "you're carrying a lot right now. "
        "Taking a short break and a few slow, deep breaths can help your "
        "mind reset. You're doing better than you think."
    ),
    "sadness": (
        "I'm really sorry you're feeling this way. "
        "It's okay to feel sad, and your feelings are completely valid. "
        "Be gentle with yourself today."
    ),
    "anxiety": (
        "Feeling anxious can be really overwhelming, and I hear you. "
        "Try grounding yourself with a few slow breaths — "
        "inhale for four counts, hold for four, exhale for four. "
        "You are safe right now."
    ),
    "anger": (
        "It makes sense that you're feeling angry — those emotions are "
        "telling you something important. "
        "It's okay to feel this way. "
        "When you're ready, try giving yourself a moment of space before "
        "responding to the situation."
    ),
    "fear": (
        "Feeling afraid is a very human experience, and you don't have "
        "to face it alone. "
        "Take this one moment at a time. "
        "You are stronger than this fear."
    ),
    "joy": (
        "It's wonderful that you're sharing this with me! "
        "Celebrate the good moments — they matter. "
        "I'm here with you."
    ),
}

_DEFAULT_FALLBACK = (
    "Thank you for sharing that with me — it takes courage to open up. "
    "Your feelings are completely valid, and I'm here to listen. "
    "Please be kind to yourself today."
)


def _get_fallback(emotion: dict[str, Any], screening: dict[str, Any]) -> str:
    """
    Select the most contextually appropriate pre-vetted fallback response.

    Priority
    --------
    1. risk_level high / moderate  — safety is the top concern.
    2. emotion label               — emotion-matched comfort.
    3. Generic default             — always non-empty, always safe.
    """
    risk_level    = screening.get("risk_level", "low").lower()
    emotion_label = emotion.get("label", "").lower()

    if risk_level in _FALLBACKS_BY_RISK:
        return _FALLBACKS_BY_RISK[risk_level]

    return _FALLBACKS_BY_EMOTION.get(emotion_label, _DEFAULT_FALLBACK)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def generate_response(
    message:   str,
    emotion:   dict[str, Any],
    intent:    dict[str, Any],
    screening: dict[str, Any],
    context:   dict[str, Any],
) -> dict[str, str]:
    """
    Generate a safe, empathetic response to the user's message.

    Parameters
    ----------
    message   : str  — raw user message.
    emotion   : dict — Person 1 output: {"label": str, "confidence": float}.
    intent    : dict — Person 2 output: {"intent": str, "confidence": float}.
    screening : dict — Person 1 output:
                       {"indicator": str, "confidence": float, "risk_level": str}.
    context   : dict — Person 3 output:
                       {
                           "conversation_memory": [{"role": str, "content": str}, ...],
                           "retrieved_knowledge": [{"text": str, "score": float}, ...]
                       }.

    Returns
    -------
    dict:
        {
            "response":      str,                  # text shown to the user
            "safety_status": "safe" | "flagged"    # pipeline audit field
        }
    """
    logger.info(
        "[response_generator] Generating response | emotion=%s | intent=%s | risk=%s",
        emotion.get("label"),
        intent.get("intent"),
        screening.get("risk_level"),
    )

    # ── Step 1: Build LLM message list ────────────────────────────────────
    messages = build_messages(
        message   = message,
        emotion   = emotion,
        intent    = intent,
        screening = screening,
        context   = context,
    )

    # ── Step 2: Call LLM ──────────────────────────────────────────────────
    llm_output = call_llm(messages)

    # ── Step 3: LLM unavailable → emotion-aware fallback ──────────────────
    if llm_output is None:
        fallback = _get_fallback(emotion, screening)
        logger.warning(
            "[response_generator] LLM unavailable — using fallback response."
        )
        return {"response": fallback, "safety_status": "safe"}

    # ── Step 4: Safety check on LLM output ────────────────────────────────
    safety_result = check_safety(llm_output)

    if safety_result["is_safe"]:
        logger.info("[response_generator] LLM output passed safety check.")
        return {"response": llm_output, "safety_status": "safe"}

    # ── Step 5: Unsafe → risk-sensitive fallback ───────────────────────────
    logger.warning(
        "[response_generator] LLM output FLAGGED. Reason: %s",
        safety_result["reason"],
    )
    fallback = _get_fallback(emotion, screening)
    return {"response": fallback, "safety_status": "flagged"}
