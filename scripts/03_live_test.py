import sys
from pathlib import Path
import cv2
import joblib
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.detector import HandDetector
from core.preprocessing import normalize_landmarks

MODEL_PATH = ROOT_DIR / "models" / "msl_classifier.joblib"
HAND_TASK_PATH = ROOT_DIR / "models" / "hand_landmarker.task"

DISPLAY_MAP = {
    "ka": "Ka (Sign 1)",
    "kha": "Kha (Sign 2)",
    "ga": "Ga (Sign 3)",
}


def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}. Run 02_train_model.py first.")

    clf = joblib.load(MODEL_PATH)
    detector = HandDetector(model_path=str(HAND_TASK_PATH))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0).")

    print("Live test running. Press [Q] or [ESC] to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        landmarks = detector.detect(frame)

        label_text = "No hand detected"
        box_color = (0, 0, 255)

        if landmarks is not None:
            detector.draw_landmarks(frame, landmarks)
            features = np.array(normalize_landmarks(landmarks), dtype=np.float32).reshape(1, -1)

            probs = clf.predict_proba(features)[0]
            best_idx = int(np.argmax(probs))
            pred_label = clf.classes_[best_idx]
            confidence = probs[best_idx] * 100

            if confidence >= 70.0:
                label_text = f"{DISPLAY_MAP.get(pred_label, pred_label)}: {confidence:.1f}%"
                box_color = (0, 200, 0)
            else:
                label_text = f"Uncertain ({confidence:.1f}%)"
                box_color = (0, 165, 255)

        cv2.rectangle(frame, (10, 10), (460, 65), (25, 25, 25), -1)
        cv2.putText(frame, label_text, (20, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.9, box_color, 2)

        cv2.imshow("MSL Live Prediction", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27) or cv2.getWindowProperty("MSL Live Prediction", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()