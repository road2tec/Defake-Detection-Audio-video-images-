import tensorflow as tf
import librosa
import numpy as np
import os
import threading

_model = None
_model_lock = threading.Lock()

# Use the verified working model
MODEL_PATH = r"v:\Road2Tech\Project_3\Image and Audio Real or Fake Detection System\trained\audio_classifier.h5"
ALT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "trained", "audio_classifier.h5")

def load_audio_model(model_path=MODEL_PATH):
    global _model
    with _model_lock:
        if _model is None:
            try:
                if not os.path.exists(model_path):
                    alt = os.path.abspath(ALT_MODEL_PATH)
                    print(f"Model file not found at {model_path}, trying {alt}...")
                    if os.path.exists(alt):
                        model_path = alt
                    else:
                        raise FileNotFoundError(f"Model file not found at {model_path} or {alt}")

                print(f"Loading TensorFlow model from {model_path}...")
                _model = tf.keras.models.load_model(model_path)
                print("Audio model (TensorFlow) loaded.")
                
                # Warmup
                try:
                    dummy_in = np.zeros((1, 128, 109, 1))
                    _model.predict(dummy_in, verbose=0)
                except Exception as e:
                    print(f"Warmup failed: {e}")
                    
            except Exception as e:
                print(f"Error loading audio model: {e}")
                return None
    return _model

def preprocess_audio(file_path):
    """
    Load audio -> Mel Spectrogram (DB) -> Resize/Pad to 109 -> Shape (1, 128, 109, 1)
    """
    try:
        # 1. Load Audio
        y, sr = librosa.load(file_path, duration=3.0) # Model expects ~3s? 
        # Note: test_tf used default load which is 22050 usually.
        # test_tf showed 'Input Shape: (None, 128, 109, 1)' and worked.
        # We will use default librosa load (22050) as evidenced by the working test.
        
        # 2. To Mel Spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # 3. Shape handling (128, 109)
        target_width = 109
        if mel_db.shape[1] < target_width:
             padding = target_width - mel_db.shape[1]
             mel_db = np.pad(mel_db, ((0, 0), (0, padding)), mode='constant')
        else:
             mel_db = mel_db[:, :target_width]
             
        # 4. Add Channel and Batch Dimensions
        # (128, 109) -> (1, 128, 109, 1)
        mel_in = mel_db[np.newaxis, ..., np.newaxis]
        
        return mel_in
        
    except Exception as e:
        print(f"Error preprocessing audio: {e}")
        return None
