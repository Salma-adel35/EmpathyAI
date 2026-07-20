from typing import Dict, List


# Stores conversation messages for each user
conversation_store: Dict[str, List[dict]] = {}


def add_message(user_id: str, role: str, content: str) -> None:
    """
    Add a message to a user's conversation history.

    Parameters:
        user_id (str): Unique identifier for the user.
        role (str): Either "user" or "assistant".
        content (str): The message content.
    """

    if user_id not in conversation_store:
        conversation_store[user_id] = []

    conversation_store[user_id].append({
        "role": role,
        "content": content
    })


def get_conversation_context(
    user_id: str,
    max_messages: int = 6
) -> List[dict]:
    """
    Retrieve the most recent messages for a user.
    """

    if user_id not in conversation_store:
        return []

    return conversation_store[user_id][-max_messages:]


def clear_memory(user_id: str) -> None:
    """
    Clear all conversation history for a user.
    """

    if user_id in conversation_store:
        del conversation_store[user_id]