#Mental Health Screening Model
# Define screening model logic
# load data (Mental-Health)
import pandas as pd

url = "https://huggingface.co/datasets/ourafla/Mental-Health_Text-Classification_Dataset/resolve/main/mental_heath_unbanlanced.csv"

df = pd.read_csv(url)

df.head()
df.info()
df.head()
df["status"].value_counts()
df = df.drop(columns=["Unique_ID"])
label_mapping = {
    "Normal": 0,
    "Depression": 1,
    "Suicidal": 2,
    "Anxiety": 3
}

df["label"] = df["status"].map(label_mapping)

# train_test_split
from sklearn.model_selection import train_test_split

# train 80% , temp 20%
train_df, temp_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# validation 10% , test 10%
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.5,
    random_state=42,
    stratify=temp_df["label"]
)

print(train_df.shape)
print(val_df.shape)
print(test_df.shape)

# tokenizer:
from .preprocessing import tokenizer
from torch.utils.data import Dataset, DataLoader


class ScreeningDataset(Dataset):

    def __init__(self, dataframe):
        self.texts = dataframe["text"].tolist()
        self.labels = dataframe["label"].tolist()


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
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "label": self.labels[idx]
        }
train_dataset = ScreeningDataset(train_df)
val_dataset = ScreeningDataset(val_df)
test_dataset = ScreeningDataset(test_df)


train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=16
)

test_loader = DataLoader(
    test_dataset,
    batch_size=16
)
batch = next(iter(train_loader))

print(batch["input_ids"].shape)
print(batch["attention_mask"].shape)
print(batch["label"].shape)

# Mental-Health model
import torch.nn as nn
from transformers import AutoModel


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


    def forward(self, input_ids, attention_mask):

        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        cls_output = outputs.last_hidden_state[:, 0, :]

        logits = self.classifier(cls_output)

        return logits



# Train screening_model
import torch
from torch.optim import AdamW


def train_screening_model(
    model,
    train_loader,
    val_loader,
    epochs=3,
    lr=2e-5
):

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model.to(device)


    optimizer = AdamW(
        model.parameters(),
        lr=lr
    )


    loss_function = torch.nn.CrossEntropyLoss()


    for epoch in range(epochs):

        model.train()
        total_loss = 0


        for batch in train_loader:

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)


            optimizer.zero_grad()


            outputs = model(
                input_ids,
                attention_mask
            )


            loss = loss_function(
                outputs,
                labels
            )


            loss.backward()

            optimizer.step()


            total_loss += loss.item()


        print(
            f"Epoch {epoch+1} Loss: {total_loss/len(train_loader)}"
        )


        evaluate_screening_model(
            model,
            val_loader,
            device
        )



def evaluate_screening_model(
    model,
    data_loader,
    device
):

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for batch in data_loader:

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)


            outputs = model(
                input_ids,
                attention_mask
            )


            predictions = torch.argmax(
                outputs,
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

    return accuracy



# ===============================
# Training and Saving
# ===============================

if __name__ == "__main__":

    screening_model = ScreeningModel(
        num_labels=4
    )

    print(screening_model)


    train_screening_model(
        screening_model,
        train_loader,
        val_loader,
        epochs=3
    )


from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent

MODEL_PATH = MODULE_DIR / "models" / "screening_model.pt"
TOKENIZER_PATH = MODULE_DIR / "models" / "screening_tokenizer"

MODEL_PATH.parent.mkdir(exist_ok=True)

torch.save(
    screening_model.state_dict(),
    MODEL_PATH
)

tokenizer.save_pretrained(
    TOKENIZER_PATH
)

print(f"Model saved to: {MODEL_PATH}")
print(f"Tokenizer saved to: {TOKENIZER_PATH}")
