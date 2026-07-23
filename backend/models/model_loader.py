from emotion_module.predict import predict_emotion
from emotion_module.screening_predict import predict_screening


def load_person1_model():

    print("Loading Emotion Model...")

    return predict_emotion


def load_person2_model():

    print("Loading Screening Model...")

    return predict_screening