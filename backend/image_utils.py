from PIL import Image
import tensorflow as tf
import numpy as np
import os
import piexif

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

_image_model = None

# Verified Absolute Path for this workspace
IMAGE_MODEL_PATH = r"v:\Road2Tech\Project_3\Image and Audio Real or Fake Detection System\trained\face_real_vs_ai_model.h5"
ALT_IMAGE_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trained", "face_real_vs_ai_model.h5")

def load_image_model(model_path=IMAGE_MODEL_PATH):
    global _image_model
    if _image_model is None:
        try:
            # 1. Try Primary Path
            if not os.path.exists(model_path):
                alt = os.path.abspath(ALT_IMAGE_MODEL_PATH)
                print(f"DEBUG: Image Model not found at {model_path}, trying {alt}...")
                if os.path.exists(alt):
                    model_path = alt
                else:
                    # Final attempts in common relative locations
                    if os.path.exists('trained/novelty.h5'):
                        model_path = 'trained/novelty.h5'
                    elif os.path.exists('../trained/novelty.h5'):
                        model_path = '../trained/novelty.h5'
                    else:
                        print(f"CRITICAL ERROR: Image Model file not found anywhere!")
                        return None
            
            print(f"DEBUG: Loading IMAGE model from: {model_path}")
            _image_model = tf.keras.models.load_model(model_path)
            
            # Verify input shape to prevent audio/image mismatch
            input_shape = _image_model.input_shape
            if len(input_shape) == 4 and input_shape[1] == 128:
                 print("CRITICAL WARNING: The file novelty.h5 appears to be an AUDIO model!")
                 _image_model = None
                 return None

            print(f"SUCCESS: Image model loaded from: {model_path}")
        except Exception as e:
            print(f"CRITICAL ERROR loading image model: {e}")
            return None
    return _image_model

def check_ai_watermark(image_path):
    """
    Check for Gemini/Google AI watermarks in metadata or common AI markers.
    Returns (is_fake, confidence, reason)
    """
    try:
        img = Image.open(image_path)
        
        # Comprehensive list of AI-related keywords to flag
        ai_keywords = ["google", "gemini", "synthetic", "ai-generated", "dall-e", "midjourney", "stable diffusion", "stablediffusion", "artificial", "adobe firefly", "synthid"]
        
        # 1. Search in image info (metadata like EXIF/IPTC)
        info = img.info
        if info:
            metadata_str = str(info).lower()
            for kw in ai_keywords:
                if kw in metadata_str:
                    print(f"AI Metadata Found: {kw}")
                    return True, 0.99, f"AI watermark ({kw}) detected in metadata"

        # 2. String search in raw file content (binary headers/XMP packets)
        try:
            with open(image_path, 'rb') as f:
                # Read the start and end of the file where XMP/IPTC is usually stored
                content = f.read(1024 * 50).lower() # First 50KB
                for kw in ai_keywords:
                    if kw.encode() in content:
                        print(f"AI String Found in File Content: {kw}")
                        return True, 0.99, f"AI-generated trace ({kw}) found in file"
        except Exception as e:
            print(f"Raw byte search error: {e}")

        return False, 0.0, "No obvious AI watermark detected"
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

