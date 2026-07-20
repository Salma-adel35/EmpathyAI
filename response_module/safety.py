"""
Safety check layer to inspect responses for harmful content,
medical advice, unsafe recommendations, or misleading claims.
"""

import re

# Patterns indicating unsafe content
UNSAFE_PATTERNS = [

    # ---------------------------------------------------------
    # Medical diagnosis
    # ---------------------------------------------------------
    r"\b(i diagnose you|diagnose you with|diagnosed with|you have|suffer from)\b.*\b(clinical\s+)?(depression|anxiety disorder|ptsd|bipolar|schizophrenia|ocd)\b",

    # ---------------------------------------------------------
    # Medication recommendations or prescriptions
    # ---------------------------------------------------------
    r"\b(take|taking|recommend|recommended|prescribe|prescribing)\b.*\b(xanax|lexapro|prozac|zoloft|adderall|valium|medication)\b",

    # Medication dosage
    r"\b\d+\s*mg\b",

    # ---------------------------------------------------------
    # Dangerous / Self-harm advice
    # ---------------------------------------------------------
    r"\b(kill yourself|end your life|hurt yourself|suicide|self-harm)\b",

    # ---------------------------------------------------------
    # Judgmental / Dismissive language
    # ---------------------------------------------------------
    r"\b(you are overreacting|stop complaining|get over it|it's not a big deal|you should be ashamed|you're just lazy)\b",

    # ---------------------------------------------------------
    # False human identity claims
    # ---------------------------------------------------------
    r"\b(as a human|i am human|i have a body|i personally experienced|when i was a child)\b",
]


def check_response_safety(response: str) -> dict:
    """
    Evaluates a generated response against safety policies.

    Parameters
    ----------
    response : str
        Generated assistant response.

    Returns
    -------
    dict
        {
            "is_safe": bool,
            "reason": str
        }
    """

    # Empty response
    if not response or not response.strip():
        return {
            "is_safe": False,
            "reason": "Empty or missing response."
        }

    # Check each unsafe pattern (case-insensitive)
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return {
                "is_safe": False,
                "reason": f"Unsafe content detected (matched rule: {pattern})"
            }

    return {
        "is_safe": True,
        "reason": "Response passed safety checks."
    }


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------
if __name__ == "__main__":

    test_responses = [

        "I diagnose you with clinical depression and recommend taking 20mg Prozac.",

        "You should kill yourself.",

        "Stop complaining and get over it.",

        "As a human, I know exactly how you feel.",

        "It sounds like you're going through a difficult time. I'm here to listen."
    ]

    for text in test_responses:
        result = check_response_safety(text)

        print("=" * 70)
        print("Response :", text)
        print("Safe     :", result["is_safe"])
        print("Reason   :", result["reason"])