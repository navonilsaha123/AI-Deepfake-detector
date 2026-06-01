from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from PIL import Image
import numpy as np

from model_loader import load_model
from utils import preprocess, analyze_artifacts
from config import THRESHOLD

app = Flask(__name__)
CORS(app)

model = load_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@app.route("/")
def home():
    return "Deepfake Detection API Running"


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        image = Image.open(file.stream).convert("RGB")
    except:
        return jsonify({"error": "Invalid image"}), 400

    image_np = np.array(image)

    # -----------------------
    # MODEL PREDICTION
    # -----------------------
    input_tensor = preprocess(image).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output).item()

    confidence = round(prob * 100, 2)
    is_fake = prob > THRESHOLD

    # -----------------------
    # FORENSIC FEATURES
    # -----------------------
    edge_score, noise_score = analyze_artifacts(image_np)

    # -----------------------
    # RESPONSE
    # -----------------------
    return jsonify({
        "verdict": "FAKE" if is_fake else "REAL",
        "confidence": confidence,
        "analysis": {
            "edge_score": edge_score,
            "noise_score": noise_score,
            "resolution": f"{image_np.shape[1]}x{image_np.shape[0]}",
            "model": "EfficientNet-B4"
        }
    })


if __name__ == "__main__":
    app.run(debug=True)