"""
Hybrid Video Deepfake Detection
Combines Xception Neural Network with Heuristic Calibration
for accurate detection of modern AI-generated videos.
"""
import torch
import torch.nn as nn
import cv2
import numpy as np
import os
from xception import Xception
from facenet_pytorch import MTCNN
from PIL import Image
import warnings

warnings.filterwarnings("ignore")

# Global models
_video_model = None
_mtcnn = None
MODEL_PATH = r"v:\Road2Tech\Project_3\Image and Audio Real or Fake Detection System\trained\ffpp_c23.pth"


def get_video_model():
    """Load Xception model trained on FaceForensics++"""
    global _video_model
    if _video_model is None:
        if not os.path.exists(MODEL_PATH):
            print(f"Video model not found at {MODEL_PATH}")
            return None
        
        try:
            print(f"Loading Xception model from {MODEL_PATH}...")
            model = Xception(num_classes=2)
            
            checkpoint = torch.load(MODEL_PATH, map_location='cpu')
            if isinstance(checkpoint, dict):
                state_dict = checkpoint.get('model', checkpoint.get('state_dict', checkpoint))
            else:
                state_dict = checkpoint
            
            # Remap keys
            new_state_dict = {}
            for k, v in state_dict.items():
                name = k
                if name.startswith('model.'):
                    name = name[6:]
                if 'last_linear' in name:
                    name = name.replace('last_linear', 'fc')
                    if 'last_linear.1' in k:
                        name = name.replace('fc.1', 'fc')
                new_state_dict[name] = v
            
            model.load_state_dict(new_state_dict, strict=False)
            model.eval()
            _video_model = model
            print("Xception model loaded successfully.")
            
        except Exception as e:
            print(f"Error loading video model: {e}")
            return None
    return _video_model


def get_mtcnn():
    """Get MTCNN face detector"""
    global _mtcnn
    if _mtcnn is None:
        try:
            _mtcnn = MTCNN(select_largest=True, post_process=False, device='cpu')
        except Exception as e:
            print(f"Error loading MTCNN: {e}")
            return None
    return _mtcnn


def preprocess_face(face_img):
    """Preprocess face for Xception model using ImageNet normalization"""
    img = cv2.resize(face_img, (299, 299))
    img = img.astype(np.float32) / 255.0
    
    # ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (img - mean) / std
    
    img = np.transpose(img, (2, 0, 1))
    return torch.tensor(img, dtype=torch.float32).unsqueeze(0)


def analyze_video(video_path, num_frames=8):
    """
    Hybrid Analysis: Xception Neural Network + Heuristic Calibration
    
    Returns both model predictions and heuristic signals for accurate detection.
    """
    print(f"[Hybrid] Analyzing video: {video_path}")
    
    model = get_video_model()
    mtcnn = get_mtcnn()
    
    if model is None or mtcnn is None:
        return {"error": "Models not ready"}
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Cannot open video"}
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        frame_count = 100
    
    indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)
    
    # Collect data for both model and heuristics
    model_predictions = []
    face_sizes = []
    face_positions = []
    face_detected_count = 0
    
    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Resize for faster processing
        h, w = frame.shape[:2]
        if w > 640:
            scale = 640 / w
            frame = cv2.resize(frame, (640, int(h * scale)))
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        
        try:
            boxes, probs = mtcnn.detect(pil_img)
        except:
            continue
        
        if boxes is not None and len(boxes) > 0:
            face_detected_count += 1
            box = boxes[0]
            x1, y1, x2, y2 = [int(b) for b in box]
            
            # Collect heuristic data
            face_width = x2 - x1
            face_height = y2 - y1
            face_area = face_width * face_height
            face_center_x = (x1 + x2) / 2
            face_center_y = (y1 + y2) / 2
            face_sizes.append(face_area)
            face_positions.append((face_center_x, face_center_y))
            
            # Clamp coordinates
            h, w = frame_rgb.shape[:2]
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            
            if x2 - x1 < 20 or y2 - y1 < 20:
                continue
            
            face = frame_rgb[y1:y2, x1:x2]
            
            # Model prediction
            input_tensor = preprocess_face(face)
            with torch.no_grad():
                logits = model(input_tensor)
                probs = torch.softmax(logits, dim=1).squeeze().tolist()
                model_predictions.append(probs)
    
    cap.release()
    
    if not model_predictions or face_detected_count < 2:
        return {"result": "UNKNOWN", "confidence": 0.0, "detail": "Insufficient face data"}
    
    # === NEURAL NETWORK ANALYSIS ===
    avg_probs = np.mean(model_predictions, axis=0)
    nn_fake_prob = avg_probs[0]  # Class 0 tendency
    nn_real_prob = avg_probs[1]  # Class 1 tendency
    
    # === HEURISTIC ANALYSIS ===
    size_variance = np.std(face_sizes) / (np.mean(face_sizes) + 1e-6)
    pos_x = [p[0] for p in face_positions]
    pos_y = [p[1] for p in face_positions]
    pos_variance = (np.std(pos_x) + np.std(pos_y)) / 2
    detection_rate = face_detected_count / num_frames
    
    heuristic_fake_score = 0.0
    
    # AI-generated videos are too consistent
    if size_variance < 0.20:
        heuristic_fake_score += 0.4
    if pos_variance < 40:
        heuristic_fake_score += 0.3
    if detection_rate > 0.9:
        heuristic_fake_score += 0.15
    
    # High variance = manipulation artifacts
    if size_variance > 0.45:
        heuristic_fake_score += 0.3
    if pos_variance > 80:
        heuristic_fake_score += 0.2
    
    # === HYBRID DECISION ===
    # Combine neural network output with heuristic calibration
    # Heuristics override when they detect strong AI patterns
    
    print(f"[Hybrid] NN Probs: {avg_probs}, Heuristic Score: {heuristic_fake_score:.2f}")
    print(f"[Hybrid] Size Var: {size_variance:.4f}, Pos Var: {pos_variance:.2f}")
    
    if heuristic_fake_score >= 0.5:
        # Heuristics detected AI-generated pattern - override NN
        label = "FAKE"
        confidence = min(0.95, 0.5 + heuristic_fake_score)
        method = "Heuristic Override"
    else:
        # Use neural network prediction
        if nn_fake_prob > nn_real_prob:
            label = "FAKE"
            confidence = float(nn_fake_prob)
        else:
            label = "REAL"
            confidence = float(nn_real_prob)
        method = "Neural Network"
    
    print(f"[Hybrid] Final: {label} ({confidence:.2f}) via {method}")
    
    return {
        "result": label,
        "confidence": float(confidence),
        "method": method,
        "nn_probs": avg_probs.tolist(),
        "heuristic_score": heuristic_fake_score
    }


def predict_video(video_path, num_frames=8):
    """Main entry point for video prediction"""
    return analyze_video(video_path, num_frames)


if __name__ == "__main__":
    print("Hybrid Video Detection Module (Xception + Heuristics)")
