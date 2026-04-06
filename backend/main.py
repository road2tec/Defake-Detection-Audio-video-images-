from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from database import connect_db, get_db, close_db
import datetime
import random
import numpy as np
from audio_utils import load_audio_model, preprocess_audio
from bson import ObjectId

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Use the existing get_db helper to interact with collections
db = get_db()
users_col = db["users"]
history_col = db["history"]

@app.post("/register")
async def register(user: User):
    if users_col.find_one({"email": user.email}):
        return {"error": "User already exists"}
    
    users_col.insert_one(user.dict())
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email, "password": req.password})
    if not user:
        return {"error": "Invalid credentials"}
    
    return {
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }

@app.get("/history/{email}")
async def get_history(email: str):
    history = list(history_col.find({"user_email": email}).sort("timestamp", -1))
    # Convert ObjectId to string for JSON serialization
    for item in history:
        item["_id"] = str(item["_id"])
    return {"history": history}

@app.delete("/history/{item_id}")
async def delete_history_item(item_id: str):
    try:
        result = history_col.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            return {"error": "Item not found"}
        return {"message": "Item deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/history/clear/{email}")
async def clear_history(email: str):
    try:
        result = history_col.delete_many({"user_email": email})
        return {"message": f"Deleted {result.deleted_count} items"}
    except Exception as e:
        return {"error": str(e)}

# Existing models and setup...

# Hold loaded models in app.state for reuse between requests
app.state.audio_model = None

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    close_db()

@app.on_event("startup")
async def startup_event():
    # Attempt to connect DB (if implemented) and preload audio model
    try:
        connect_db()
    except Exception as e:
        print(f"Warning: connect_db() failed on startup: {e}")

    try:
        print("Preloading audio model on startup...")
        m = load_audio_model()
        if m is not None:
            app.state.audio_model = m
            print("Audio model preloaded and stored on app.state.audio_model")
        else:
            print("Audio model returned None on preload. Will attempt lazy load on first request.")
    except Exception as e:
        print(f"Error preloading audio model: {e}")

@app.post("/predict")
def predict_file(file: UploadFile = File(...), user_email: Optional[str] = None):
    filename = file.filename
    content_type = file.content_type
    print(f"DEBUG: Filename={filename}, Content-Type={content_type}")
    
    if content_type is None:
        content_type = "application/octet-stream"

    label = "PROCESSING_ERROR"
    confidence = 0.0
    
    # Save temp file for processing (librosa needs path)
    import shutil
    import os
    temp_filename = f"temp_{filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(f"File Save Error: {e}")
        return {"error": "file_save_failed", "detail": str(e)}
    try:
        if content_type.startswith("audio/"):
            # Audio Prediction Logic
            print("Processing Audio...")
            # Try to reuse preloaded model
            model = getattr(app.state, 'audio_model', None)
            if model is None:
                print("No preloaded model found; attempting to load now...")
                model = load_audio_model()
                app.state.audio_model = model
            if model:
                segments = preprocess_audio(temp_filename)
                if segments:
                    # Batch prediction for efficiency
                    batch = np.vstack(segments)
                    print(f"Analyzing {len(segments)} audio segments (Batch shape: {batch.shape})...")
                    
                    try:
                        probs = model.predict(batch, verbose=0) # [N, 2]
                        # Average probabilities across all segments
                        avg_probs = np.mean(probs, axis=0)
                    except Exception as e:
                         print(f"Model prediction error: {e}")
                         raise e

                    print(f"AVERAGE PREDICTION (Probs): {avg_probs}")
                    
                    fake_prob = float(avg_probs[0])
                    real_prob = float(avg_probs[1])
                    
                    if real_prob > fake_prob:
                        label = "REAL"
                        confidence = real_prob
                    else:
                        label = "FAKE"
                        confidence = fake_prob

                    print(f"Result: {label} (REAL_PROB: {real_prob:.4f}, FAKE_PROB: {fake_prob:.4f})")
                else:
                    print("Feature extraction failed.")
                    return {"error": "Could not extract features"}
            else:
                print("Audio model refused to load.")
                return {"error": "model_not_loaded", "detail": "Audio model could not be loaded. Check server logs and model file."}

        elif content_type.startswith("image/"):
             # Image Prediction Logic
             print("Processing Image...")
             print("Processing Image...")
             from image_utils import load_image_model, preprocess_image, check_ai_watermark
             
             # 1. First check for AI watermarks (Gemini/Google)
             is_ai, water_conf, reason = check_ai_watermark(temp_filename)
             if is_ai:
                 print(f"Watermark Detection: {reason}")
                 label = "FAKE"
                 confidence = water_conf
             else:
                 # 2. Falling back to ML model if no metadata watermark found
                 model = load_image_model()
                 if model:
                     print("Image Model loaded. Preprocessing...")
                     img_tensor = preprocess_image(temp_filename)
                     if img_tensor is not None:
                         print(f"Image processed: {img_tensor.shape}. Predicting...")
                         pred = model.predict(img_tensor)
                         print(f"Prediction raw: {pred}")
                         
                         # Assume binary sigmoid output [0=Fake, 1=Real] or similar
                         score = float(pred[0][0]) if pred.shape[-1] == 1 else float(pred[0][1])
                         confidence = score if score > 0.5 else 1 - score
                         label = "REAL" if score > 0.5 else "FAKE"
                         print(f"Result: {label} ({confidence})")
                     else:
                         return {"error": "Could not process image"}
                 else:
                    return {"error": "model_load_failed", "detail": "Image detection model failed to load. Check trained/ folder."}


        
        elif content_type.startswith("video/"):
             # Video Prediction - Hybrid Detection (Xception + Heuristics)
             print("Processing Video (Hybrid Neural + Heuristic)...")
             from video_utils import predict_video
             video_result = predict_video(temp_filename)
             
             if "error" in video_result:
                 label = "ERROR"
                 confidence = 0.0
                 print(f"Video Error: {video_result['error']}")
             else:
                 label = video_result['result']
                 confidence = float(video_result['confidence'])
                 print(f"Video Result: {label} ({confidence}) Raw: {video_result.get('raw')}")
        else:
             return {"error": "Unsupported media type"}
             
    except Exception as e:
        print(f"Prediction Error: {e}")
        return {"error": "prediction_failed", "detail": str(e)}
    # Process cleanup
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    
    result_data = {
        "filename": filename,
        "label": label,
        "confidence": confidence,
        "content_type": content_type,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Save to history if user is logged in
    if user_email:
        try:
            history_col.insert_one({
                "user_email": user_email,
                **result_data
            })
            print(f"Saved history for {user_email}")
        except Exception as e:
            print(f"Error saving history: {e}")

    return result_data
