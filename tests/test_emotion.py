from predict import predict_mental_health

def run_pipeline():

    text = input("Enter your text: ")

    result = predict_mental_health(text)

    print("\n===== Mental Health Analysis =====")

    print("Text:")
    print(result["text"])

    print("\nEmotion:")
    print(
        result["emotion"]["label"],
        "- Confidence:",
        result["emotion"]["confidence"], "%"
    )

    print("\nScreening:")
    print(
        result["screening"]["label"],
        "- Confidence:",
        result["screening"]["confidence"], "%"
    )


# Run
run_pipeline()
