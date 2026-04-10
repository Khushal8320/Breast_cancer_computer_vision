"""
model_utils.py
Handles model loading and inference for the Breast Cancer Detection app.
Supports both .pth (PyTorch state_dict) and .pkl (pickle) model files.
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import pickle
import io
import numpy as np

# ── Label mapping ──────────────────────────────────────────────────────────────
CLASS_NAMES   = {0: "Normal", 1: "Cancer Detected"}
CLASS_COLORS  = {0: "#2ecc71", 1: "#e74c3c"}
CLASS_ICONS   = {0: "✅", 1: "⚠️"}

# ── Image preprocessing (matches training pipeline) ───────────────────────────
INFERENCE_TRANSFORM = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std =[0.229, 0.224, 0.225]
    )
])


def _build_architecture(num_classes: int = 2) -> nn.Module:
    """Build a ResNet-18 with a custom head (mirrors training code)."""
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def load_model(model_path: str) -> nn.Module:
    """
    Load model from .pth (state_dict) or .pkl (pickle) file.
    Returns the model in eval mode on CPU.
    """
    if model_path.endswith(".pkl"):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    else:  # .pth / .pt
        model = _build_architecture(num_classes=2)
        state = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state)

    model.eval()
    return model


def load_model_from_bytes(file_bytes: bytes, filename: str) -> nn.Module:
    """Load model from uploaded bytes (Streamlit file uploader)."""
    if filename.endswith(".pkl"):
        model = pickle.loads(file_bytes)
    else:
        model = _build_architecture(num_classes=2)
        state = torch.load(io.BytesIO(file_bytes), map_location="cpu")
        model.load_state_dict(state)

    model.eval()
    return model


def predict(model: nn.Module, image: Image.Image) -> dict:
    """
    Run inference on a single PIL image.

    Returns:
        {
          "class_id":    int,
          "label":       str,
          "confidence":  float  (0-100),
          "probabilities": {0: float, 1: float}
        }
    """
    tensor = INFERENCE_TRANSFORM(image.convert("RGB")).unsqueeze(0)

    with torch.no_grad():
        logits = model(tensor)
        probs  = torch.softmax(logits, dim=1).squeeze().numpy()

    class_id   = int(np.argmax(probs))
    confidence = float(probs[class_id]) * 100

    return {
        "class_id":      class_id,
        "label":         CLASS_NAMES[class_id],
        "confidence":    confidence,
        "probabilities": {i: float(probs[i]) * 100 for i in range(len(probs))},
        "color":         CLASS_COLORS[class_id],
        "icon":          CLASS_ICONS[class_id],
    }
