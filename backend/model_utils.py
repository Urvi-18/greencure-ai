import io
import json
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
device = torch.device("cpu")

with open(MODEL_DIR / "class_names.json") as f:
    CLASS_NAMES = json.load(f)


def load_model():
    m = models.mobilenet_v2(weights=None)
    m.classifier = nn.Sequential(nn.Dropout(0.2), nn.Linear(m.last_channel, len(CLASS_NAMES)))
    m.load_state_dict(torch.load(MODEL_DIR / "best_model.pt", map_location=device))
    m.eval()
    return m


model = load_model()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def predict(image_bytes: bytes, top_k: int = 3):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    x = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1)[0]
    conf, idx = torch.topk(probs, top_k)
    return [
        {"class": CLASS_NAMES[i], "confidence": round(c, 4)}
        for c, i in zip(conf.tolist(), idx.tolist())
    ]