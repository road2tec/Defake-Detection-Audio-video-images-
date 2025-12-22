import tensorflow as tf
import numpy as np
import os

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

_model = None

def load_image_model(model_path='backend/novelty.h5'):
    global _model
    if _model is None:
        try:
            # Try local path if backend path fails (or vice versa depending on cwd)
            if not os.path.exists(model_path):
                if os.path.exists('novelty.h5'):
                    model_path = 'novelty.h5'
                else:
                    print(f"Image model file not found at {model_path}")
                    return None
                    
            _model = tf.keras.models.load_model(model_path)
            print("Image model loaded.")
        except Exception as e:
            print(f"Error loading image model: {e}")
    return _model

def preprocess_image(file_path):
    """
    Load image, resize to [256, 256], and normalize.
    """
    target_size = (256, 256)
    
    try:
        # Load image using generic TF or PIL
        img = tf.keras.utils.load_img(file_path, target_size=target_size)
        img_array = tf.keras.utils.img_to_array(img)
        
        # Normalize (assuming 0-1 range is expected, standard for generic CNNs)
        # If model expects -1 to 1 (e.g. ResNet preprocessing), this might be wrong.
        # Without training code, 0-1 / 255.0 is the safest guess.
        img_array = img_array / 255.0
        
        # Add batch dimension: (1, 256, 256, 3)
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None
