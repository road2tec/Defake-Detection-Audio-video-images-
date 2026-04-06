import tensorflow as tf
import librosa
import numpy as np
import os
import threading

_audio_model = None
_model_lock = threading.Lock()

# Use the verified working model
MODEL_PATH = r"v:\Road2Tech\Project_3\Image and Audio Real or Fake Detection System\trained\audio_classifier.h5"
ALT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "trained", "audio_classifier.h5")

def load_audio_model(model_path=MODEL_PATH):
    global _audio_model
    with _model_lock:
        if _audio_model is None:
            try:
                if not os.path.exists(model_path):
                    alt = os.path.abspath(ALT_MODEL_PATH)
                    print(f"DEBUG: Audio Model file not found at {model_path}, trying {alt}...")
                    if os.path.exists(alt):
                        model_path = alt
                    else:
                        raise FileNotFoundError(f"Audio Model file not found at {model_path} or {alt}")

                print(f"DEBUG: Loading AUDIO model strictly from {model_path}...")
                _audio_model = tf.keras.models.load_model(model_path)
                print("SUCCESS: Audio model (TensorFlow) loaded.")
                
                # Warmup
                try:
                    dummy_in = np.zeros((1, 128, 109, 1))
                    _audio_model.predict(dummy_in, verbose=0)
                except Exception as e:
                    print(f"Audio Warmup failed (minor): {e}")
                    
            except Exception as e:
                print(f"CRITICAL ERROR loading audio model: {e}")
                return None
    return _audio_model


def preprocess_audio(file_path, max_segments=10):
    """
    Load audio -> Split into segments of 3s -> For each: Mel Spectrogram (DB) -> Resize/Pad to 109 -> Shape (1, 128, 109, 1)
    Returns a list of tensors for all segments.
    """
    try:
        # 1. Load entire Audio (or up to 5 mins if supported)
        y, sr = librosa.load(file_path, duration=300.0) # Up to 5 mins
        
        duration = librosa.get_duration(y=y, sr=sr)
        segment_len = 3.0 # seconds
        
        segments = []
        
        # Calculate start points for segments (limit to max_segments for speed)
        # We can take samples at equal intervals
        num_possible_segments = int(duration // segment_len)
        if num_possible_segments <= 0:
            num_possible_segments = 1
            
        step = max(1, num_possible_segments // max_segments)
        
        for i in range(0, num_possible_segments, step):
            start = i * int(segment_len * sr)
            end = (i + 1) * int(segment_len * sr)
            
            if start >= len(y):
                break
                
            y_segment = y[start:min(end, len(y))]
            
            # Mel Spectrogram
            mel_spec = librosa.feature.melspectrogram(y=y_segment, sr=sr, n_mels=128)
            mel_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Shape handling (128, 109)
            target_width = 109
            if mel_db.shape[1] < target_width:
                 padding = target_width - mel_db.shape[1]
                 mel_db = np.pad(mel_db, ((0, 0), (0, padding)), mode='constant')
            else:
                 mel_db = mel_db[:, :target_width]
                 
            # Add dimensions
            mel_in = mel_db[np.newaxis, ..., np.newaxis]
            segments.append(mel_in)
            
            if len(segments) >= max_segments:
                break
                
        return segments # Return list of processed segment tensors
        
    except Exception as e:
        print(f"Error preprocessing audio: {e}")
        return None

