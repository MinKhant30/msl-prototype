import csv
import sys
from pathlib import Path
import cv2

# Allow importing from project root (`core/`)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.detector import HandDetector
from core.preprocessing import normalize_landmarks

DATA_PATH = ROOT_DIR / "data" / "raw" / "landmarks.csv"

# Key bindings -> (label_id, display_name)
SIGN_MAP = {
    ord("1"): ("ka", "Sign 1: Ka"),
    ord("2"): ("kha", "Sign 2: Kha"),
    ord("3"): ("ga", "Sign 3: Ga"),
}


def init_csv(csv_path: Path):
    """Create CSV with header if it doesn't exist yet."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        header = ["label"] + [f"{axis}{i}" for i in range(21) for axis in ("x", "y", "z")]
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)


def count_existing_samples(csv_path: Path) -> dict[str, int]:
    """Count saved rows per class so you know your dataset balance."""
    counts = {"ka": 0, "kha": 0, "ga": 0}
    if not csv_path.exists():
        return counts
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if row and row[0] in counts:
                counts[row[0]] += 1
    return counts


def main():
    init_csv(DATA_PATH)
    counts = count_existing_samples(DATA_PATH)
    detector = HandDetector(model_path=str(ROOT_DIR / "models" / "hand_landmarker.task"))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0).")

    print("=== MSL Data Collector ===")
    print("Hold [1] to record Ka (က) | Hold [2] to record Kha (ခ) | Hold [3] to record Ga (ဂ)")
    print("Press [Q] or [ESC] to quit.")

    with open(DATA_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Mirror image so signing feels natural
            frame = cv2.flip(frame, 1)
            landmarks = detector.detect(frame)

            status_text = "No hand detected"
            status_color = (0, 0, 255)

            if landmarks is not None:
                detector.draw_landmarks(frame, landmarks)
                status_text = "Hand Ready - Hold 1 (Ka), 2 (Kha), or 3 (Ga)"
                status_color = (0, 255, 0)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):  # 'q' or ESC
                break

            # Record sample while key 1, 2, or 3 is pressed AND a hand is visible
            if key in SIGN_MAP and landmarks is not None:
                label_id, display_name = SIGN_MAP[key]
                features = normalize_landmarks(landmarks)
                writer.writerow([label_id] + features)
                counts[label_id] += 1
                status_text = f"RECORDING {display_name}..."
                status_color = (0, 215, 255)

            # HUD Overlay
            cv2.rectangle(frame, (10, 10), (620, 95), (25, 25, 25), -1)
            cv2.putText(frame, status_text, (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            summary = f"Counts -> Ka: {counts['ka']} | Kha: {counts['kha']} | Ga: {counts['ga']}"
            cv2.putText(frame, summary, (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

            cv2.imshow("MSL Data Collector", frame)

    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved dataset to {DATA_PATH}. Final counts: {counts}")


if __name__ == "__main__":
    main()