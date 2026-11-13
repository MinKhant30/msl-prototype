from contextlib import asynccontextmanager
from pathlib import Path
import cv2
import joblib
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import LandmarkRequest, PredictionResponse
from core.detector import HandDetector
from core.preprocessing import normalize_landmarks

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / "models" / "msl_classifier.joblib"
HAND_TASK_PATH = ROOT_DIR / "models" / "hand_landmarker.task"

MYANMAR_CHAR_MAP = {
    "ka": "က",
    "kha": "ခ",
    "ga": "ဂ",
}

ml_resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Missing classifier at {MODEL_PATH}. Run scripts/02_train_model.py first.")
    ml_resources["classifier"] = joblib.load(MODEL_PATH)
    ml_resources["detector"] = HandDetector(model_path=str(HAND_TASK_PATH))
    yield
    ml_resources.clear()


app = FastAPI(
    title="Myanmar Sign Language (MSL) Static Prototype API",
    version="0.1.0",
    lifespan=lifespan,
)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(STATIC_DIR / "index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def classify_features(features: list[float]) -> PredictionResponse:
    clf = ml_resources["classifier"]
    arr = np.array(features, dtype=np.float32).reshape(1, -1)
    probs = clf.predict_proba(arr)[0]

    best_idx = int(np.argmax(probs))
    label_id = str(clf.classes_[best_idx])
    confidence = round(float(probs[best_idx]), 4)
    prob_dict = {str(cls): round(float(p), 4) for cls, p in zip(clf.classes_, probs)}

    return PredictionResponse(
        hand_detected=True,
        label_id=label_id,
        myanmar_char=MYANMAR_CHAR_MAP.get(label_id),
        confidence=confidence,
        probabilities=prob_dict,
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "supported_signs": MYANMAR_CHAR_MAP}


@app.post("/predict/landmarks", response_model=PredictionResponse)
def predict_from_landmarks(payload: LandmarkRequest):
    """Fast inference endpoint when the client already extracted 63 normalized landmarks."""
    return classify_features(payload.landmarks)


@app.post("/predict/image", response_model=PredictionResponse)
async def predict_from_image(file: UploadFile = File(...)):
    """Accepts an uploaded image frame (JPEG/PNG), detects the hand, and classifies the sign."""
    contents = await file.read()
    np_buf = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_buf, cv2.IMREAD_COLOR)

    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    landmarks = ml_resources["detector"].detect(frame)
    if landmarks is None:
        return PredictionResponse(hand_detected=False)

    features = normalize_landmarks(landmarks)
    return classify_features(features)