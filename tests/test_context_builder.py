from context_module.context_builder import build_full_context


def test_build_full_context():

    message = (
        "I feel really overwhelmed "
        "about my exam."
    )

    emotion_result = {
        "emotion": {
            "label": "stress",
            "confidence": 0.91
        },
        "screening": {
            "indicator": "stress_related",
            "confidence": 0.80
        },
        "risk_level": "low"
    }

    intent_result = {
        "intent": "seeking_support",
        "confidence": 0.89
    }

    context_result = {
        "conversation_memory": [
            {
                "role": "user",
                "content": "I have an exam tomorrow."
            }
        ],
        "retrieved_knowledge": [
            {
                "text": (
                    "Breaking large tasks "
                    "into smaller steps may help."
                ),
                "score": 0.92
            }
        ]
    }

    result = build_full_context(
        message=message,
        emotion_result=emotion_result,
        intent_result=intent_result,
        context_result=context_result
    )

    assert result["message"] == message

    assert result["emotion"]["label"] == "stress"

    assert (
        result["screening"]["indicator"]
        == "stress_related"
    )

    assert result["risk_level"] == "low"

    assert (
        result["intent"]
        == "seeking_support"
    )

    assert len(
        result["conversation_memory"]
    ) == 1

    assert len(
        result["retrieved_knowledge"]
    ) == 1


if __name__ == "__main__":
    test_build_full_context()

    print(
        "Context builder test passed successfully!"
    )