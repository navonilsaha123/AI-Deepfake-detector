import numpy as np
import cv2
from PIL import Image
import torchvision.transforms as transforms
from config import IMAGE_SIZE

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
])

def preprocess(image):
    return transform(image).unsqueeze(0)

def analyze_artifacts(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    edge_score = float(np.mean(edges))

    noise_score = float(np.std(image_np))

    return edge_score, noise_score