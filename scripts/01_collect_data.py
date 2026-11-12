import csv
import json
import sys
from datetime import datetime
from pathlib import Path
import cv2

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.detector import HandDetector
from core.preprocessing import normalize_landmarks
from core.team_roster import TEAM_MEMBERS

DATA_DIR = ROOT_DIR / "data" / "raw"
SESSION_FILE = ROOT_DIR / ".collector_session.json"

SIGN_MAP = {
    ord("1"): ("ka", "Sign 1: Ka"),
    ord("2"): ("kha", "Sign 2: Kha"),
    ord("3"): ("ga", "Sign 3: Ga"),
}

HEADER = ["member_key", "collector", "timestamp", "label"] + [
    f"{axis}{i}" for i in range(21) for axis in ("x", "y", "z")
]


def authenticate_member() -> tuple[str, dict]:
    """Load saved member session if available; otherwise prompt once for access key."""
    if SESSION_FILE.exists():
        try:
            saved = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            key = saved.get("member_key", "").lower()
            if key in TEAM_MEMBERS:
                member = TEAM_MEMBERS[key]
                print(f"Welcome back, {member['name']} ({key})!")
                return key, member
        except (json.JSONDecodeError, OSError):
            pass

    while True:
        entered_key = input("Enter your unique Team Access Key (e.g., smm123): ").strip().lower()
        if entered_key in TEAM_MEMBERS:
            member = TEAM_MEMBERS[entered_key]
            SESSION_FILE.write_text(
                json.dumps({"member_key": entered_key}, indent=2),
                encoding="utf-8",
            )
            print(f"Verified! Logged in as {member['name']} (saved for future sessions).")
            return entered_key, member
        print("Invalid access key. Please check your key with the team leader and try again.")


def load_existing_rows(csv_path: Path) -> list[list]:
    if not csv_path.exists():
        return []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        return [row for row in reader if row]


def save_all_rows(csv_path: Path, rows: list[list]):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)


def get_counts(rows: list[list]) -> dict[str, int]:
    counts = {"ka": 0, "kha": 0, "ga": 0}
    for row in rows:
        if len(row) >= 4 and row[3] in counts:
            counts[row[3]] += 1
    return counts


def main():
    member_key, member = authenticate_member()
    csv_path = DATA_DIR / f"landmarks_{member['slug']}.csv"

    all_rows = load_existing_rows(csv_path)
    if not csv_path.exists():
        save_all_rows(csv_path, all_rows)

    burst_history: list[int] = []
    current_burst_count = 0
    was_recording = False
    banner_frames = 0
    banner_msg = ""

    detector = HandDetector(model_path=str(ROOT_DIR / "models" / "hand_landmarker.task"))
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0).")

    print(f"Saving to: {csv_path.name}")
    print("Hold [1] Ka | Hold [2] Kha | Hold [3] Ga | [Z] Undo Last Burst | [L] Switch Account | [Q] Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        landmarks = detector.detect(frame)

        status_text = "No hand detected"
        status_color = (0, 0, 255)

        if landmarks is not None:
            detector.draw_landmarks(frame, landmarks)
            status_text = "Hold [1] Ka, [2] Kha, [3] Ga | [Z] Undo | [L] Switch User"
            status_color = (0, 255, 0)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break

        # Switch user account if sharing a laptop
        if key == ord("l"):
            if SESSION_FILE.exists():
                SESSION_FILE.unlink()
            print("Logged out. Run the script again to log in with another member key.")
            break

        # Undo last recorded burst
        if key == ord("z") and burst_history:
            removed_count = burst_history.pop()
            all_rows = all_rows[:-removed_count]
            save_all_rows(csv_path, all_rows)
            banner_msg = f"UNDID last {removed_count} samples!"
            banner_frames = 45

        if key in SIGN_MAP and landmarks is not None:
            label_id, display_name = SIGN_MAP[key]
            features = normalize_landmarks(landmarks)
            timestamp = datetime.now().isoformat(timespec="seconds")
            all_rows.append([member_key, member["slug"], timestamp, label_id] + features)

            current_burst_count += 1
            was_recording = True
            status_text = f"RECORDING {display_name} (+{current_burst_count})"
            status_color = (0, 215, 255)
        else:
            if was_recording and current_burst_count > 0:
                burst_history.append(current_burst_count)
                save_all_rows(csv_path, all_rows)
                current_burst_count = 0
                was_recording = False

        if banner_frames > 0:
            status_text = banner_msg
            status_color = (255, 180, 0)
            banner_frames -= 1

        counts = get_counts(all_rows)
        cv2.rectangle(frame, (10, 10), (635, 95), (25, 25, 25), -1)
        cv2.putText(frame, status_text, (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        summary = f"{member['name']} | Ka: {counts['ka']} | Kha: {counts['kha']} | Ga: {counts['ga']}"
        cv2.putText(frame, summary, (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("MSL Data Collector", frame)
        if cv2.getWindowProperty("MSL Data Collector", cv2.WND_PROP_VISIBLE) < 1:
            break

    if was_recording and current_burst_count > 0:
        save_all_rows(csv_path, all_rows)

    cap.release()
    cv2.destroyAllWindows()
    print(f"Finished! {member['name']} now has {len(all_rows)} total rows in {csv_path.name}")


if __name__ == "__main__":
    main()