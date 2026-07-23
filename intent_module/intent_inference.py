"""
EmpathyAI - Intent Detection inference module.

Public interface:
    predict_intent(text: str) -> dict
        Returns {"label": <one of the 5 intent labels>, "confidence": <float 0-1>}

This module loads the fine-tuned DistilBERT model saved alongside this file
(in the same directory) and exposes a single, simple prediction function for
downstream EmpathyAI modules (Memory & RAG, orchestrator, etc.) to import.
"""

import os

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

_MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_tokenizer = AutoTokenizer.from_pretrained(_MODEL_DIR)
_model = AutoModelForSequenceClassification.from_pretrained(_MODEL_DIR)
_model.to(_DEVICE)
_model.eval()

_ID2LABEL = _model.config.id2label
_MAX_LENGTH = 128


def predict_intent(text: str) -> dict:
    """
    Predict the conversational intent of a single user message.

    Args:
        text: Raw user message.

    Returns:
        dict: {"label": str, "confidence": float}  # confidence in [0, 1]

    Raises:
        ValueError: if `text` is not a non-empty string.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    inputs = _tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=_MAX_LENGTH,
    )
    inputs = {k: v.to(_DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        logits = _model(**inputs).logits
        probs = torch.softmax(logits, dim=-1).squeeze(0)

    pred_id = int(torch.argmax(probs).item())
    confidence = float(probs[pred_id].item())

    if isinstance(_ID2LABEL, dict):
        label = _ID2LABEL.get(pred_id, _ID2LABEL.get(str(pred_id)))
    else:
        label = _ID2LABEL[pred_id]

    return {"label": label, "confidence": round(confidence, 4)}


if __name__ == "__main__":
    sample = "I don\'t know what to do anymore, can you help me think this through?"
    print(predict_intent(sample))
