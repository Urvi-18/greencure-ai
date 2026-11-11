import io
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
USE_ONNX = os.environ.get("USE_ONNX", "0") == "1"

with open(MODEL_DIR / "class_names.json") as f:
    CLASS_NAMES = json.load(f)

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

if USE_ONNX:
    # Light runtime used for hosting: no PyTorch needed.
    import onnxruntime as ort

    _session = ort.InferenceSession(
        str(MODEL_DIR / "model.onnx"), providers=["CPUExecutionProvider"]
    )

    def _logits(img):
        resized = img.resize((224, 224), Image.Resampling.BILINEAR)
        arr = np.asarray(resized, dtype=np.float32) / 255.0
        arr = ((arr - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
        return _session.run(None, {"input": arr})[0][0]
else:
    # Original PyTorch path used locally.
    import torch
    import torch.nn as nn
    from torchvision import models, transforms

    device = torch.device("cpu")

    def load_model():
        m = models.mobilenet_v2(weights=None)
        m.classifier = nn.Sequential(
            nn.Dropout(0.2), nn.Linear(m.last_channel, len(CLASS_NAMES))
        )
        m.load_state_dict(torch.load(MODEL_DIR / "best_model.pt", map_location=device))
        m.eval()
        return m

    model = load_model()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    def _logits(img):
        x = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            return model(x)[0].numpy()


def _softmax(x):
    x = x.astype(np.float64)
    e = np.exp(x - x.max())
    return e / e.sum()


def predict(image_bytes: bytes, top_k: int = 3):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    probs = _softmax(_logits(img))
    idx = np.argsort(probs)[::-1][:top_k]
    return [
        {"class": CLASS_NAMES[i], "confidence": round(float(probs[i]), 4)}
        for i in idx
    ]
