import re
from datasets import load_dataset
from transformers import AutoTokenizer
from torch.utils.data import Dataset, DataLoader


MODEL_NAME = "bert-base-uncased"


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


def load_emotion_dataset():

    return load_dataset(
        "dair-ai/emotion"
    )


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


class EmotionDataset(Dataset):

    def __init__(self, dataset):

        self.texts = dataset["text"]

        self.labels = dataset["label"]


    def __len__(self):

        return len(self.texts)


    def __getitem__(self, idx):

        encoding = tokenizer(
            self.texts[idx],
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": self.labels[idx]
        }


def create_dataloaders(
    dataset,
    batch_size=16
):

    train_dataset = EmotionDataset(
        dataset["train"]
    )

    val_dataset = EmotionDataset(
        dataset["validation"]
    )

    test_dataset = EmotionDataset(
        dataset["test"]
    )


    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size
    )


    return (
        train_loader,
        val_loader,
        test_loader
    )