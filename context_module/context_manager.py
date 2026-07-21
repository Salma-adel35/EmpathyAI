from typing import Dict, Any

from .memory import get_conversation_context
from .rag import retrieve_relevant_context


def get_context(
    user_id: str,
    query: str,
    top_k: int = 3
) -> Dict[str, Any]:
    """
    Retrieve conversation memory and relevant knowledge.

    This module is responsible only for:
    - Conversation memory
    - RAG retrieval

    Emotion, intent, and screening analysis are handled
    by other modules.
    """

    conversation_memory = get_conversation_context(
        user_id=user_id
    )

    retrieved_knowledge = retrieve_relevant_context(
        query=query,
        top_k=top_k
    )

    return {
        "conversation_memory": conversation_memory,
        "retrieved_knowledge": retrieved_knowledge
    }