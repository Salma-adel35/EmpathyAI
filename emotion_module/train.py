from pathlib import Path

import torch

from torch.optim import AdamW
from torch.nn import CrossEntropyLoss

from emotion_module.preprocessing import (
    load_emotion_dataset,
    create_dataloaders,
    tokenizer
)

from emotion_module.emotion_model import (
    EmotionModel
)

MODULE_DIR = Path(
    __file__
).resolve().parent


MODEL_DIR = MODULE_DIR / "models"

MODEL_DIR.mkdir(
    exist_ok=True
)

MODEL_PATH = MODEL_DIR / "emotion_model.pt"

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def evaluate(
    model,
    data_loader
):

    model.eval()


    correct = 0
    total = 0


    with torch.no_grad():

        for batch in data_loader:

            input_ids = (
                batch["input_ids"]
                .to(DEVICE)
            )


            attention_mask = (
                batch["attention_mask"]
                .to(DEVICE)
            )


            labels = (
                batch["label"]
                .to(DEVICE)
            )


            logits = model(
                input_ids,
                attention_mask
            )


            predictions = torch.argmax(
                logits,
                dim=1
            )


            correct += (
                predictions == labels
            ).sum().item()


            total += labels.size(0)


    accuracy = correct / total


    print(
        f"Validation Accuracy: {accuracy:.4f}"
    )


def train():

    print(
        f"Using device: {DEVICE}"
    )


    dataset = (
        load_emotion_dataset()
    )


    (
        train_loader,
        validation_loader,
        test_loader
    ) = create_dataloaders(
        dataset
    )


    model = EmotionModel(
        num_labels=6
    )


    model.to(DEVICE)


    optimizer = AdamW(
        model.parameters(),
        lr=2e-5
    )


    loss_function = (
        CrossEntropyLoss()
    )


    epochs = 3


    for epoch in range(epochs):

        model.train()


        total_loss = 0


        for batch in train_loader:

            input_ids = (
                batch["input_ids"]
                .to(DEVICE)
            )


            attention_mask = (
                batch["attention_mask"]
                .to(DEVICE)
            )


            labels = (
                batch["label"]
                .to(DEVICE)
            )


            optimizer.zero_grad()


            logits = model(
                input_ids,
                attention_mask
            )


            loss = loss_function(
                logits,
                labels
            )


            loss.backward()


            optimizer.step()


            total_loss += (
                loss.item()
            )


        average_loss = (
            total_loss
            / len(train_loader)
        )


        print(
            f"Epoch {epoch + 1}/{epochs}"
        )


        print(
            f"Loss: {average_loss:.4f}"
        )


        evaluate(
            model,
            validation_loader
        )


    torch.save(
        model.state_dict(),
        MODEL_PATH
    )


    tokenizer.save_pretrained(
        MODULE_DIR / "tokenizer"
    )


    print(
        f"Model saved to: {MODEL_PATH}"
    )


if __name__ == "__main__":

    train()