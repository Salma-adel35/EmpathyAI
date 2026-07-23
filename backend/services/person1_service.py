from emotion_module.predict import predict_emotion


def analyze_with_person1(model, text):

    if model is None:

        return {
            "status": "model_not_available",
            "message": "Emotion model is not available yet."
        }

    result = model(text)

    return {

        "status": "success",

        "result": result

    }