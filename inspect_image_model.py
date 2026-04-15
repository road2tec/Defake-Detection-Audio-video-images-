import tensorflow as tf
import os

model_path = 'trained/face_real_vs_ai_model.h5'
if os.path.exists(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model Summary for {model_path}:")
        model.summary()
        print("\nInput Shape:", model.input_shape)
        print("Layer Names:", [l.name for l in model.layers])
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Model not found at {model_path}")