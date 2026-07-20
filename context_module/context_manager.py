from typing import Dict

from .memory import get_conversation_context
from .rag import retrieve_relevant_context


def get_context(
    user_id: str,
    query: str
) -> Dict:
    """
    Retrieve both conversation memory
    and relevant knowledge.
    """

    conversation_memory = get_conversation_context(
        user_id=user_id
    )

    retrieved_knowledge = retrieve_relevant_context(
        query=query,
        top_k=3
    )

    return {
        "conversation_memory": conversation_memory,
        "retrieved_knowledge": retrieved_knowledge
    }