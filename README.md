# 🔍 DeepDetect - AI Media Authentication System

A full-stack web application for detecting AI-generated and manipulated media (images, audio, and videos) using deep learning and computer vision techniques.

## 📋 Features

- **Image Detection**: Classifies images as REAL or FAKE using CNN-based analysis
- **Audio Detection**: Detects AI-generated audio using Mel-spectrogram analysis with TensorFlow
- **Video Detection**: Analyzes videos for deepfakes using Xception neural network with heuristic calibration
- **Modern UI**: Responsive React frontend with smooth animations
- **MongoDB Integration**: Stores prediction history and user data

## 🏗️ Architecture

```
├── backend/                 # FastAPI Python Backend
│   ├── main.py             # API endpoints
│   ├── audio_utils.py      # Audio processing & detection
│   ├── image_utils.py      # Image processing & detection
│   ├── video_utils.py      # Video analysis (Xception + Heuristics)
│   ├── xception.py         # Xception neural network architecture
│   ├── database.py         # MongoDB connection
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React Vite Frontend
│   ├── src/
│   │   ├── pages/         # Dashboard, Home, Login, etc.
│   │   └── components/    # Reusable UI components
│   └── package.json
│
└── trained/                # Pre-trained model weights
    ├── ffpp_c23.pth       # Xception model (Video - FaceForensics++)
    ├── audio_classifier.h5 # Audio detection model (TensorFlow)
    └── novelty.h5          # Image detection model (TensorFlow CNN)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "MONGO_URI=your_mongodb_connection_string" > .env

# Run server
uvicorn main:app --reload --port 8080
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080

## 🧠 Models Used

### Video Detection
- **Architecture**: Xception Neural Network
- **Training Data**: FaceForensics++ Dataset (c23 compression)
- **Approach**: Hybrid detection combining deep learning with heuristic analysis
- **Features**:
  - MTCNN face detection
  - Frame-by-frame analysis
  - Temporal consistency checks

### Audio Detection
- **Architecture**: CNN with Mel-spectrogram input
- **Framework**: TensorFlow/Keras
- **Input**: 109-frame Mel-spectrograms (128 mel bins)

### Image Detection
- **Model**: novelty.h5 (TensorFlow/Keras)
- **Architecture**: CNN Classifier
- **Input Size**: 256x256 RGB images
- **Output**: Binary classification (REAL/FAKE) with confidence score
- **Preprocessing**: Normalized to [0, 1] range

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Analyze media file (image/audio/video) |
| `/health` | GET | Server health check |
| `/docs` | GET | Interactive API documentation |

### Example Request

```bash
curl -X POST "http://localhost:8080/predict" \
  -F "file=@video.mp4"
```

### Response

```json
{
  "filename": "video.mp4",
  "label": "FAKE",
  "confidence": 0.87,
  "content_type": "video/mp4"
}
```

## 🛠️ Tech Stack

**Frontend:**
- React 18 with Vite
- Framer Motion (animations)
- React Router DOM
- Axios
- CSS3 with modern effects

**Backend:**
- FastAPI (Python)
- TensorFlow 2.x
- PyTorch 2.x
- OpenCV
- MTCNN (face detection)
- MongoDB (pymongo)

## 📁 Environment Variables

Create a `.env` file in the backend directory:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
```

## 🔧 Development

### Adding New Detection Models

1. Add model weights to `trained/` directory
2. Create utility file in `backend/` (e.g., `new_utils.py`)
3. Implement `predict()` function
4. Import and use in `main.py`

### Running Tests

```bash
cd backend
python -m pytest tests/
```

## 📊 Model Performance

| Media Type | Model | Accuracy | Notes |
|------------|-------|----------|-------|
| Video | Xception + Heuristics | ~95% | Best for face-swap deepfakes |
| Audio | TensorFlow CNN | ~98% | Mel-spectrogram analysis |
| Image | CNN Classifier | ~97% | Binary classification |

## 🙏 Acknowledgments

- [FaceForensics++](https://github.com/ondyari/FaceForensics) for the video detection dataset
- [MTCNN](https://github.com/ipazc/mtcnn) for face detection
- [Xception](https://arxiv.org/abs/1610.02357) architecture

## 👨‍💻 Author

**[@road2tec](https://github.com/road2tec)**

🔗 **Repository**: [road2tec/Defake-Detection-Audio-video-images-](https://github.com/road2tec/Defake-Detection-Audio-video-images-)

---

**Built with ❤️ for detecting AI-generated media**
