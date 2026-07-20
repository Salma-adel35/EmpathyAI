import sys
import os

# Add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from response_module.response_pipeline import process_response
from response_module.safety import check_response_safety

def run_tests():
    print("=" * 60)
    print("EMPATHY AI — RESPONSE MODULE TESTS")
    print("=" * 60 + "\n")

    test_cases = [
        {
            "name": "Test 1: Anxiety + Seeking Support",
            "message": "I studied all day but I still feel like I am going to fail.",
            "emotion": {"label": "anxiety", "confidence": 0.91},
            "intent": {"label": "seeking_support", "confidence": 0.94},
            "memory": [{"role": "user", "content": "I have an exam tomorrow."}],
            "rag": [{"text": "Deep breathing and grounding exercises reduce exam anxiety.", "score": 0.88}]
        },
        {
            "name": "Test 2: Sadness + Venting",
            "message": "My best friend moved away today and I just feel so alone.",
            "emotion": {"label": "sadness", "confidence": 0.95},
            "intent": {"label": "venting", "confidence": 0.92},
            "memory": [],
            "rag": []
        },
        {
            "name": "Test 3: Stress + Seeking Advice",
            "message": "I have 5 assignments due tomorrow and don't know where to start.",
            "emotion": {"label": "stress", "confidence": 0.89},
            "intent": {"label": "seeking_advice", "confidence": 0.91},
            "memory": [],
            "rag": [{"text": "Prioritizing tasks using time-blocking lowers overwhelm.", "score": 0.82}]
        },
        {
            "name": "Test 4: Happiness + Casual Conversation",
            "message": "I just adopted a kitten today! She's sleeping on my lap.",
            "emotion": {"label": "happiness", "confidence": 0.98},
            "intent": {"label": "casual_conversation", "confidence": 0.96},
            "memory": [],
            "rag": []
        },
        {
            "name": "Test 5: Anxiety + Seeking Motivation",
            "message": "I have to give a speech in an hour and my hands are trembling.",
            "emotion": {"label": "anxiety", "confidence": 0.93},
            "intent": {"label": "seeking_motivation", "confidence": 0.90},
            "memory": [],
            "rag": []
        }
    ]

    for tc in test_cases:
        print(f"📌 {tc['name']}")
        print(f"User Message: \"{tc['message']}\"")
        result = process_response(
            message=tc["message"],
            emotion=tc["emotion"],
            intent=tc["intent"],
            conversation_memory=tc["memory"],
            retrieved_knowledge=tc["rag"]
        )
        print(f"Response: {result['response']}")
        print(f"Status  : {result['safety_status']}\n")
        print("-" * 60)

    # Test Safety Trigger Interception
    print("\n📌 Safety Rule Trap Test")
    unsafe_text = "I diagnose you with clinical depression and recommend taking 20mg Prozac."
    safety = check_response_safety(unsafe_text)
    print(f"Input: \"{unsafe_text}\"")
    print(f"Safety Inspection: {safety}")

if __name__ == "__main__":
    run_tests()