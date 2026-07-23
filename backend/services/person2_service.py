def analyze_with_person2(model, text):

    if model is None:

        return {

            "status": "model_not_available",

            "message": "Screening model is not available yet."

        }

    result = model(text)

    return {

        "status": "success",

        "result": result

    }