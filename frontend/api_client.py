import requests

from config import (
    BACKEND_URL,
    USE_MOCK_API
)


def get_mock_response(message: str) -> dict:
    """
    Temporary response used during frontend development.
    This will be replaced by the real backend later.
    """

    message_lower = message.lower()

    if any(
        word in message_lower
        for word in [
            "stressed",
            "stress",
            "overwhelmed",
            "exam"
        ]
    ):
        emotion = "Stress"
        emotion_emoji = "😣"

        response = (
            "It sounds like you are feeling overwhelmed right now. "
            "You do not have to handle everything at once. "
            "Taking things one step at a time can make things feel more manageable."
        )

    elif any(
        word in message_lower
        for word in [
            "sad",
            "unhappy",
            "lonely"
        ]
    ):
        emotion = "Sadness"
        emotion_emoji = "😔"

        response = (
            "I hear you. It sounds like you are going through "
            "a difficult moment, and it is okay to express how you feel."
        )

    elif any(
        word in message_lower
        for word in [
            "anxious",
            "anxiety",
            "worried",
            "scared"
        ]
    ):
        emotion = "Anxiety"
        emotion_emoji = "😟"

        response = (
            "It sounds like you are feeling anxious right now. "
            "You do not have to solve everything immediately. "
            "Let's take things one step at a time."
        )

    elif any(
        word in message_lower
        for word in [
            "happy",
            "excited",
            "great"
        ]
    ):
        emotion = "Happiness"
        emotion_emoji = "😊"

        response = (
            "That sounds wonderful! "
            "I am glad to hear that things are going well for you."
        )

    else:
        emotion = "Neutral"
        emotion_emoji = "🙂"

        response = (
            "I am here to listen. "
            "Tell me more about what is on your mind."
        )

    return {
        "response": response,
        "emotion": emotion,
        "emotion_emoji": emotion_emoji,
        "intent": "seeking_support",
        "memory_used": True,
        "rag_used": True,
        "safety_status": "safe"
    }


def send_message(
    message: str,
    user_id: str = "demo_user"
) -> dict:
    """
    Send a message to the EmpathyAI backend.

    During development:
        USE_MOCK_API=true

    After backend deployment:
        USE_MOCK_API=false
    """

    if USE_MOCK_API:
        return get_mock_response(message)

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "user_id": user_id,
                "message": message
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        return {
            "response": (
                "I am having trouble connecting to the "
                "EmpathyAI service right now. Please try again."
            ),
            "emotion": "Unknown",
            "emotion_emoji": "⚪",
            "intent": "unknown",
            "memory_used": False,
            "rag_used": False,
            "safety_status": "fallback",
            "error": str(error)
        }