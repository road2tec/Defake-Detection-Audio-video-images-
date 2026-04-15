import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the model
MODEL_PATH = 'trained/face_real_vs_ai_model.h5'
model = load_model(MODEL_PATH)

# Preprocess the image
def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize to [0, 1]
    return img_array

# Predict function
def predict(img_path):
    img = preprocess_image(img_path)
    pred = model.predict(img)
    # Assuming binary classification: 0 = Real, 1 = Fake
    label = 'Fake' if pred[0][0] > 0.5 else 'Real'
    print(f'Prediction: {label} (score={pred[0][0]:.4f})')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python detect_face_real_or_fake.py <image_path>')
        sys.exit(1)
    img_path = sys.argv[1]
    predict(img_path)
