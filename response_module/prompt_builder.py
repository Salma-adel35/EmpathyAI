"""
prompt_builder.py
=================
Constructs the system prompt and user prompt sent to the LLM.

All four upstream contract outputs (emotion, intent, screening, context)
are woven together here into a structured prompt pair so the LLM has
full situational awareness before generating a response.
"""

from typing import Any

# ── Intent → behavioural directive mapping ────────────────────────────────
# Maps Person 2's intent label into an explicit instruction for the LLM so
# it adapts its style to what the user actually needs right now.
_INTENT_DIRECTIVES: dict[str, str] = {
    "seeking_support": "Offer warm emotional validation and gentle encouragement.",
    "venting":         "Listen empathetically. Do NOT give advice unless asked.",
    "seeking_advice":  "Provide practical, evidence-based coping suggestions.",
    "seeking_info":    "Give clear, factual information while remaining warm.",
    "crisis":          "Respond with calm reassurance and refer to professional help.",
    "casual_chat":     "Respond in a friendly, light, and supportive tone.",
}
_DEFAULT_DIRECTIVE = "Respond with empathy and care."

# ── Risk level → escalation instruction ───────────────────────────────────
_RISK_NOTES: dict[str, str] = {
    "low": "",
    "moderate": (
        "The user may be experiencing significant distress. "
        "Gently acknowledge their feelings and mention that speaking to "
        "a counsellor or trusted person can be helpful."
    ),
    "high": (
        "The user may be in serious distress. "
        "Prioritise their safety above all else. "
        "Calmly encourage them to contact a crisis helpline or "
        "mental-health professional immediately."
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
def build_system_prompt(
    emotion:   dict[str, Any],
    intent:    dict[str, Any],
    screening: dict[str, Any],
) -> str:
    """
    Build the system prompt that governs the LLM's persona and hard constraints.

    Parameters
    ----------
    emotion   : {"label": str, "confidence": float}
    intent    : {"intent": str, "confidence": float}
    screening : {"indicator": str, "confidence": float, "risk_level": str}
    """
    intent_label     = intent.get("intent", "seeking_support")
    intent_directive = _INTENT_DIRECTIVES.get(intent_label, _DEFAULT_DIRECTIVE)
    emotion_label    = emotion.get("label", "distress")
    emotion_conf     = emotion.get("confidence", 0.0)
    risk_level       = screening.get("risk_level", "low").lower()
    risk_note        = _RISK_NOTES.get(risk_level, "")
    screening_note   = (
        f" Consider that the user's screening indicator is "
        f"'{screening.get('indicator', 'unknown')}'."
        if risk_level != "low" else ""
    )

    return f"""\
You are EmpathyAI, a compassionate emotional support assistant.
Your role is to provide a safe, non-judgmental, empathetic space for users.

CURRENT USER CONTEXT:
- Detected emotion  : {emotion_label} (confidence: {emotion_conf:.0%})
- Detected intent   : {intent_label}
- Risk level        : {risk_level}{screening_note}

BEHAVIOURAL DIRECTIVE FOR THIS RESPONSE:
{intent_directive}
{risk_note}

ABSOLUTE RULES — YOU MUST NEVER VIOLATE THESE:
1. NEVER diagnose the user with any mental illness or medical condition.
   Do NOT say things like "You have depression", "This sounds like anxiety disorder", etc.
2. NEVER prescribe, recommend, or name any medication or drug.
3. NEVER say anything harmful, dismissive, or judgmental about the user's feelings.
4. NEVER claim to be a therapist, psychologist, or medical professional.
5. Keep your response concise: 2 to 4 sentences only.
6. Always validate the user's emotions before offering any suggestions.
7. If the risk level is 'high', always recommend professional or crisis support.""".strip()


# ─────────────────────────────────────────────────────────────────────────────
def build_user_prompt(
    message: str,
    context: dict[str, Any],
) -> str:
    """
    Build the user-turn prompt carrying the current message plus enriched
    context from Person 3 (conversation memory + RAG knowledge).

    Parameters
    ----------
    message : str — the raw user message.
    context : {
        "conversation_memory": [{"role": str, "content": str}, ...],
        "retrieved_knowledge": [{"text": str, "score": float}, ...]
    }
    """
    # ── Conversation history (Person 3 memory) ────────────────────────────
    memory: list[dict] = context.get("conversation_memory", [])
    history_block = ""
    if memory:
        lines = [
            f"  [{t.get('role', 'user').capitalize()}]: {t.get('content', '').strip()}"
            for t in memory
            if t.get("content", "").strip()
        ]
        if lines:
            history_block = "RECENT CONVERSATION HISTORY:\n" + "\n".join(lines)

    # ── Retrieved knowledge (Person 3 RAG) ────────────────────────────────
    # Only include snippets above relevance threshold 0.50
    knowledge: list[dict] = context.get("retrieved_knowledge", [])
    relevant = [k for k in knowledge if k.get("score", 0.0) >= 0.50]
    knowledge_block = ""
    if relevant:
        klines = [f"  - {k['text'].strip()}" for k in relevant]
        knowledge_block = (
            "RELEVANT SUPPORT KNOWLEDGE "
            "(use subtly if helpful, never quote verbatim):\n"
            + "\n".join(klines)
        )

    # ── Assemble ──────────────────────────────────────────────────────────
    parts = []
    if history_block:
        parts.append(history_block)
    if knowledge_block:
        parts.append(knowledge_block)
    parts.append(f"USER'S CURRENT MESSAGE:\n  {message.strip()}")
    parts.append("Please respond empathetically to the user's current message.")

    return "\n\n".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
def build_messages(
    message:   str,
    emotion:   dict[str, Any],
    intent:    dict[str, Any],
    screening: dict[str, Any],
    context:   dict[str, Any],
) -> list[dict[str, str]]:
    """
    Assemble the complete OpenAI-style messages list for llm_client.

    Returns
    -------
    [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
    """
    return [
        {"role": "system", "content": build_system_prompt(emotion, intent, screening)},
        {"role": "user",   "content": build_user_prompt(message, context)},
    ]
