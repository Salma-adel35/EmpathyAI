from response_module.response_pipeline import process_response


def generate_response(
    user_message,
    person1_result,
    person2_result,
    intent_result,
    conversation_memory,
    retrieved_knowledge
):

    emotion = person1_result.get(
        "result",
        {}
    )

    response_result = process_response(

        message=user_message,

        emotion=emotion,

        intent=intent_result or {},

        conversation_memory=conversation_memory,

        retrieved_knowledge=retrieved_knowledge

    )

    return {

        "user_message": user_message,

        "person1_analysis": person1_result,

        "person2_analysis": person2_result,

        "intent_analysis": intent_result,

        "response": response_result["response"],

        "safety_status": response_result["safety_status"],

        "retrieved_knowledge": retrieved_knowledge

    }