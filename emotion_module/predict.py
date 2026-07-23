from pathlib import Path

import torch
import torch.nn.functional as F

from emotion_module.preprocessing import tokenizer
from emotion_module.emotion_model import EmotionModel


MODULE_DIR = Path(
    __file__
).resolve().parent


MODEL_PATH = (
    MODULE_DIR
    / "models"
    / "emotion_model.pt"
)


DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


emotion_model = EmotionModel(
    num_labels=6
)


emotion_model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)


emotion_model.to(
    DEVICE
)


emotion_model.eval()


ID2EMOTION = {

    0: "sadness",

    1: "joy",

    2: "love",

    3: "anger",

    4: "fear",

    5: "surprise"
}


def predict_emotion(
    text: str
) -> dict:

    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )


    input_ids = (
        encoding["input_ids"]
        .to(DEVICE)
    )


    attention_mask = (
        encoding["attention_mask"]
        .to(DEVICE)
    )


    with torch.no_grad():

        logits = emotion_model(
            input_ids,
            attention_mask
        )


        probabilities = F.softmax(
            logits,
            dim=1
        )


        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )


    return {

        "label": ID2EMOTION[
            prediction.item()
        ],

        "confidence": round(
            confidence.item(),
            4
        )

    }


def predict_mental_health(
    text: str
) -> dict:

    emotion_result = (
        predict_emotion(text)
    )


    return {

        "text": text,

        "emotion": emotion_result

    }