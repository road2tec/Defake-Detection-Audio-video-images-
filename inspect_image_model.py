import tensorflow as tf
import numpy as np

model_path = r'v:\Road2Tech\Project_3\Image and Audio Real or Fake Detection System\trained\audio_classifier.h5'
try:
    model = tf.keras.models.load_model(model_path)
    print("--- MODEL INFO START ---")
    print(f"MODEL_PATH: {model_path}")
    print(f"INPUT_SHAPE: {model.input_shape}")
    print(f"OUTPUT_SHAPE: {model.output_shape}")
    print("--- MODEL INFO END ---")
    # model.summary()
    
    # Check prediction on dummy data
    dummy_input = np.random.rand(1, 256, 256, 3) * 255.0
    
    # Method 1: [0, 1]
    in1 = dummy_input / 255.0
    pred1 = model.predict(in1, verbose=0)
    print(f"Norm [0, 1] -> {pred1}")
    
    # Method 2: [-1, 1]
    in2 = (dummy_input / 127.5) - 1.0
    pred2 = model.predict(in2, verbose=0)
    print(f"Norm [-1, 1] -> {pred2}")

    # Method 3: No normalization
    in3 = dummy_input
    pred3 = model.predict(in3, verbose=0)
    print(f"Norm None -> {pred3}")
    
except Exception as e:
    print(f"Error: {e}")
