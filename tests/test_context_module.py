from context_module.memory import add_message
from context_module.context_manager import get_context


user_id = "user_1"


# Add previous conversation
add_message(
    user_id=user_id,
    role="user",
    content="I have an exam tomorrow."
)


add_message(
    user_id=user_id,
    role="assistant",
    content="That sounds stressful."
)


add_message(
    user_id=user_id,
    role="user",
    content="I feel really overwhelmed."
)


# Get combined context
context = get_context(
    user_id=user_id,
    query="I feel stressed about my exam."
)


print("\n" + "=" * 60)
print("CONVERSATION MEMORY")
print("=" * 60)


for message in context["conversation_memory"]:
    print(
        f"{message['role']}: "
        f"{message['content']}"
    )


print("\n" + "=" * 60)
print("RETRIEVED KNOWLEDGE")
print("=" * 60)


for index, item in enumerate(
    context["retrieved_knowledge"],
    start=1
):

    print(f"\nResult {index}")
    print(f"Distance: {item['score']}")
    print(f"Text: {item['text']}")