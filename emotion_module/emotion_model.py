import torch
import torch.nn as nn
from transformers import AutoModel


class EmotionModel(nn.Module):

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

        cls_output = (
            outputs.last_hidden_state[:, 0, :]
        )

        logits = self.classifier(
            cls_output
        )

        return logits