from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoModel

from emotion_module.preprocessing import tokenizer


class ScreeningModel(nn.Module):

    def __init__(self, num_labels):

        super().__init__()

        self.bert = AutoModel.from_pretrained(
            "bert-base-uncased"
        )

        self.classifier = nn.Linear(
            self.bert.config.hidden_size,
            num_labels
        )

    def forward(
        self,
        input_ids,
        attention_mask
    ):

        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        cls_output = outputs.last_hidden_state[:, 0, :]

        logits = self.classifier(
            cls_output
        )

        return logits


MODULE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    MODULE_DIR
    / "models"
    / "screening_model.pt"
)


DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


screening_model = ScreeningModel(
    num_labels=4
)


screening_model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)


screening_model.to(DEVICE)

screening_model.eval()


ID2STATUS = {

    0: "Normal",

    1: "Depression",

    2: "Suicidal",

    3: "Anxiety"

}


def predict_screening(
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

        logits = screening_model(
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

        "label": ID2STATUS[
            prediction.item()
        ],

        "confidence": round(
            confidence.item(),
            4
        )

    }