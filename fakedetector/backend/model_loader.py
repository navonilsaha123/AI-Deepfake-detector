import torch
import timm
from config import MODEL_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    model = timm.create_model("efficientnet_b4", pretrained=True)

    # ✅ BEST FIX (no errors, version-safe)
    model.reset_classifier(num_classes=1)

    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    except:
        print("⚠️ Using pretrained weights (no custom model found)")

    model.to(device)
    model.eval()

    return model