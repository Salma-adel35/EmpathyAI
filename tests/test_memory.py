from memory import (
    add_message,
    get_conversation_context,
    clear_memory
)


user_id = "user_1"


add_message(
    user_id,
    "user",
    "I have an exam tomorrow."
)

add_message(
    user_id,
    "assistant",
    "That sounds stressful."
)

add_message(
    user_id,
    "user",
    "I am really scared."
)


context = get_conversation_context(user_id)

print("Conversation Context:")
print(context)


clear_memory(user_id)

print("\nAfter clearing memory:")
print(get_conversation_context(user_id))