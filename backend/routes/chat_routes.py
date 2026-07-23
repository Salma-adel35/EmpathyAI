from flask import Blueprint, request, jsonify

from backend.services.person1_service import analyze_with_person1
from backend.services.person2_service import analyze_with_person2
from backend.services.response_service import generate_response

from context_module.memory import (
    add_message,
    get_conversation_context
)

from context_module.rag import retrieve_relevant_context

from intent_module.intent_inference import predict_intent


chat_bp = Blueprint(
    "chat",
    __name__
)


def create_chat_route(
    person1_model,
    person2_model,
    predict_intent
):

    @chat_bp.route(
        "/chat",
        methods=["POST"]
    )
    def chat():

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is empty."
            }), 400

        user_message = data.get("message")

        if not user_message:
            return jsonify({
                "error": "Message is required."
            }), 400

        user_id = data.get(
            "user_id",
            "default_user"
        )

        # 1. Save user message
        add_message(
            user_id=user_id,
            role="user",
            content=user_message
        )

        # 2. Emotion Analysis
        person1_result = analyze_with_person1(
            person1_model,
            user_message
        )

        # 3. Mental Health Screening
        person2_result = analyze_with_person2(
            person2_model,
            user_message
        )

        # 4. Intent Analysis
        intent_result = predict_intent(
            user_message
        )

        print("INTENT:")
        print(intent_result)

        # 5. Conversation Memory
        conversation_memory = get_conversation_context(
            user_id=user_id,
            max_messages=6
        )

        print("MEMORY:")
        print(conversation_memory)

        # 6. Retrieve RAG Knowledge
        retrieved_knowledge = retrieve_relevant_context(
            user_message,
            top_k=3
        )

        print("RAG:")
        print(retrieved_knowledge)

        # 7. Generate Response
        final_response = generate_response(

            user_message=user_message,

            person1_result=person1_result,

            person2_result=person2_result,

            intent_result=intent_result,

            conversation_memory=conversation_memory,

            retrieved_knowledge=retrieved_knowledge

        )

        # 8. Save assistant response
        add_message(
            user_id=user_id,
            role="assistant",
            content=final_response["response"]
        )

        # 9. Return response
        return jsonify({

            "user_message": user_message,

            "intent_analysis": intent_result,

            "person1_analysis": person1_result,

            "person2_analysis": person2_result,

            "response": final_response["response"],

            "safety_status": final_response["safety_status"],

            "retrieved_knowledge": retrieved_knowledge

        })

    return chat_bp