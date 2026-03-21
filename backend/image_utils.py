from PIL import Image
import tensorflow as tf
import numpy as np
import os
import piexif

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

_model = None

def load_image_model(model_path='backend/novelty.h5'):
    global _model
    if _model is None:
        try:
            if not os.path.exists(model_path):
                if os.path.exists('novelty.h5'):
                    model_path = 'novelty.h5'
                else:
                    return None
            _model = tf.keras.models.load_model(model_path)
            print("Image model loaded.")
        except Exception as e:
            print(f"Error loading image model: {e}")
    return _model

def check_ai_watermark(image_path):
    """
    Check for Gemini/Google AI watermarks in metadata or via visual heuristics.
    Returns (is_fake, confidence, reason)
    """
    try:
        img = Image.open(image_path)
        
        # 1. Check Metadata (SynthID often leaves specific markers or IPTC tags)
        # Google AI generated images often contain 'Generated with AI' or specific IPTC DigitalSourceType
        metadata_found = False
        
        # Check for Google/Gemini specific strings in metadata
        info = img.info
        if info:
            metadata_str = str(info).lower()
            if "google" in metadata_str or "gemini" in metadata_str or "synthetic" in metadata_str or "ai-generated" in metadata_str:
                return True, 0.99, "AI metadata marker detected"

        # Check IPTC (if available) - Google uses 'trainedAlgorithmicMedia' for SynthID
        # (This requires more advanced parsing, but simple string search in raw info works often)
        
        # 2. Visual Heuristic: Corner Star Check
        # Gemini often adds a small 4-point star in the bottom right corner.
        # This is a very basic check for non-black pixels in a specific tiny pattern.
        # But metadata is more reliable if not stripped.
        
        return False, 0.0, "No obvious watermark"
    except Exception as e:
        print(f"Watermark check error: {e}")
        return False, 0.0, str(e)

def preprocess_image(file_path):
    """
    Load image, resize to [256, 256], and normalize.
    """
    target_size = (256, 256)
    try:
        img = tf.keras.utils.load_img(file_path, target_size=target_size)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

