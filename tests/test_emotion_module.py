from emotion_module.predict import predict_mental_health


def main():

    text = "I feel very anxious and hopeless lately"

    result = predict_mental_health(text)

    print("=" * 60)
    print("EMOTION MODULE TEST")
    print("=" * 60)

    print(result)


if __name__ == "__main__":
    main()