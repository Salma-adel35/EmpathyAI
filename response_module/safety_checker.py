"""
safety_checker.py
=================
Rule-based safety filter that inspects LLM output before it reaches the user.

Three violation categories:
  A. Diagnostic statements  — LLM claims user has a medical/psychiatric condition.
  B. Prescription language  — LLM names drugs or instructs user to take medication.
  C. Harmful / judgmental   — dismissive, stigmatising, or dangerous language.

Returns {"is_safe": bool, "reason": str} for every inspection.
"""

import re
import logging
from typing import Any

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# A. Diagnostic patterns
# Catches: "you have depression", "you are suffering from PTSD",
#          "this is bipolar disorder", "sounds like OCD"
# ─────────────────────────────────────────────────────────────────────────────
_DIAGNOSIS_PATTERNS: list[re.Pattern] = [
    # "you have / you are suffering from / you are diagnosed with / you show signs of"
    re.compile(
        r"\byou\s+(have|are\s+suffering\s+from|are\s+diagnosed\s+with|show\s+signs\s+of)\b",
        re.I,
    ),
    # "this is a sign of / symptom of / case of"
    re.compile(
        r"\bthis\s+is\s+(a\s+)?(sign\s+of|symptom\s+of|case\s+of)\b",
        re.I,
    ),
    # "sounds/seems/appears like [you have] [a] <disorder>"
    re.compile(
        r"\b(sounds?|seems?|appears?)\s+like\s+(you\s+have\s+)?(a\s+)?"
        r"(depression|anxiety\s+disorder|bipolar|schizophrenia|ptsd|"
        r"ocd|adhd|bpd|personality\s+disorder|psychosis|eating\s+disorder)\b",
        re.I,
    ),
    # "you are / might be / could be depressed / bipolar …"
    re.compile(
        r"\byou\s+(are|might\s+be|could\s+be)\s+"
        r"(depressed|bipolar|schizophrenic|psychotic|mentally\s+ill)\b",
        re.I,
    ),
    # any form of the word "diagnose"
    re.compile(r"\bdiagnos(is|ed|e|ing)\b", re.I),
    # "you suffer from"
    re.compile(r"\byou\s+suffer\s+from\b", re.I),
]

# ─────────────────────────────────────────────────────────────────────────────
# B. Prescription / medication patterns
# Catches named psychiatric drugs and prescribing language.
# ─────────────────────────────────────────────────────────────────────────────
_PRESCRIPTION_PATTERNS: list[re.Pattern] = [
    # Common psychiatric drug names and drug-class terms
    re.compile(
        r"\b(sertraline|fluoxetine|prozac|zoloft|lexapro|escitalopram|"
        r"citalopram|paroxetine|venlafaxine|duloxetine|bupropion|wellbutrin|"
        r"lithium|valproate|lamotrigine|quetiapine|seroquel|olanzapine|"
        r"risperidone|aripiprazole|clonazepam|lorazepam|diazepam|valium|"
        r"xanax|alprazolam|ativan|ambien|zolpidem|adderall|ritalin|"
        r"methylphenidate|antidepressant|antipsychotic|benzodiazepine|"
        r"ssri|snri|mood\s+stabiliser|mood\s+stabilizer)\b",
        re.I,
    ),
    # "take/use/start taking … pill/tablet/dose/mg"
    re.compile(
        r"\b(take|try|use|start\s+taking|consider\s+taking|"
        r"prescribed?|medication|medicate)\b.{0,40}"
        r"\b(drug|pill|tablet|capsule|dose|mg)\b",
        re.I,
    ),
    # any form of "prescribe" / "prescription"
    re.compile(r"\bprescri(be|bing|bed|ption)\b", re.I),
    # "you should take/use/try a medication/drug/pill/tablet"
    re.compile(
        r"\byou\s+should\s+(take|use|try)\s+(a\s+)?(medication|drug|pill|tablet)\b",
        re.I,
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# C. Harmful / judgmental patterns
# Catches dismissive, shaming, or dangerous language.
# ─────────────────────────────────────────────────────────────────────────────
_HARMFUL_PATTERNS: list[re.Pattern] = [
    # "just get over it", "stop being dramatic", "man up", "toughen up"
    re.compile(
        r"\b(just\s+)?(get\s+over\s+it|stop\s+(being\s+)?(dramatic|weak|sensitive|"
        r"negative|pathetic)|pull\s+yourself\s+together|man\s+up|toughen\s+up)\b",
        re.I,
    ),
    # "it's all in your head", "not a big deal", "overreacting"
    re.compile(
        r"\b(it('s|\s+is)\s+)?(all\s+in\s+your\s+head|not\s+a\s+big\s+deal|"
        r"not\s+that\s+serious|over(re)?acting)\b",
        re.I,
    ),
    # "you're weak / pathetic / broken / crazy …"
    re.compile(
        r"\byou('re|\s+are)\s+(weak|pathetic|broken|crazy|insane|stupid|dramatic)\b",
        re.I,
    ),
    # "nobody cares", "you don't matter"
    re.compile(
        r"\b(nobody\s+cares?|no\s+one\s+cares?|you\s+don'?t\s+matter)\b",
        re.I,
    ),
    # Self-harm instructional content the LLM must never produce
    re.compile(
        r"\b(how\s+to\s+(hurt|harm|kill|end)\s+(yourself|your\s+life)|"
        r"suicide\s+(method|plan|how\s+to))\b",
        re.I,
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
def check_safety(text: str) -> dict[str, Any]:
    """
    Inspect `text` (LLM-generated output) for safety violations.

    Parameters
    ----------
    text : str — the raw LLM response to inspect.

    Returns
    -------
    dict:
        {
            "is_safe": bool,
            "reason":  str   # "safe" if clean, otherwise a violation description.
        }
    """
    if not text or not text.strip():
        return {"is_safe": False, "reason": "Empty response from LLM."}

    # ── A. Diagnostic ─────────────────────────────────────────────────────
    for pattern in _DIAGNOSIS_PATTERNS:
        if pattern.search(text):
            reason = (
                f"Diagnostic language detected "
                f"(pattern: '{pattern.pattern[:60]}…'). "
                "EmpathyAI must never diagnose users with medical or "
                "psychiatric conditions."
            )
            logger.warning("[safety_checker] FLAGGED — diagnosis: %s", reason)
            return {"is_safe": False, "reason": reason}

    # ── B. Prescription ───────────────────────────────────────────────────
    for pattern in _PRESCRIPTION_PATTERNS:
        if pattern.search(text):
            reason = (
                f"Prescription/medication language detected "
                f"(pattern: '{pattern.pattern[:60]}…'). "
                "EmpathyAI must never recommend drugs or prescribe medication."
            )
            logger.warning("[safety_checker] FLAGGED — prescription: %s", reason)
            return {"is_safe": False, "reason": reason}

    # ── C. Harmful ────────────────────────────────────────────────────────
    for pattern in _HARMFUL_PATTERNS:
        if pattern.search(text):
            reason = (
                f"Harmful or judgmental language detected "
                f"(pattern: '{pattern.pattern[:60]}…'). "
                "EmpathyAI must always respond with empathy and never "
                "dismiss the user."
            )
            logger.warning("[safety_checker] FLAGGED — harmful: %s", reason)
            return {"is_safe": False, "reason": reason}

    return {"is_safe": True, "reason": "safe"}
