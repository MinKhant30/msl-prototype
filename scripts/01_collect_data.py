import csv
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
import cv2

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.detector import HandDetector
from core.preprocessing import normalize_landmarks

# SHA-256 hashes of member keys (safe to push to GitHub; impossible to reverse)

MEMBER_HASHES = {
    "f3eea7d9060c63dd7343d5d8bf426d31727006a78163849b24572e03c8b552ea": {
        "name": "Min Khant Nyar",
        "slug": "min_khant_nyar",
    },
    "de7cebecdbfbaedd1a99ed28bd4e85f328ef7991f30faa84305b57cdfe2161d9": {
        "name": "Soe Myat Min",
        "slug": "soe_myat_min",
    },
    "18f78be3dbc3c59d153218cf673b709945d784c822441e22dd2f200605a211bb": {
        "name": "Myat Phone Myint",
        "slug": "myat_phone_myint",
    },
    "8a8f9a43ca38ef12c95e5dc2e6e386ef5bb47654330b5e0f7c62ff6425b03a5b": {
        "name": "Aung Phyo Thu",
        "slug": "aung_phyo_thu",
    },
    "a27bb45e608bdbff2f7a7b1ef671e3bf1aba0660b4eabb6dd22c3b75df41c80b": {
        "name": "Aung Thein Khaing",
        "slug": "aung_thein_khaing",
    },
    "9a55062f91f055e7478cee3934c1b35c4ab022c5dca4a2c91447d98dd39bf9df": {
        "name": "Min Khant Kyaw Win",
        "slug": "min_khant_kyaw_win",
    },
    "0d029c08d3e68f82341ee395d4af63b8b4073a35cf66f550a21df0c0624c45a2": {
        "name": "Moe Kyaw Htike",
        "slug": "moe_kyaw_htike",
    },
    "8b341219ecbde7947091a1b60c16cef494fe4270c4ff7a7af2c2e14b9a3f655a": {
        "name": "Thurein Theikdi Soe",
        "slug": "thurein_theikdi_soe",
    },
    "5a55b5e954a7821d358b9233e6f6388e55370d798781e5a28ea5d9dcec8a239e": {
        "name": "Khin Hla",
        "slug": "khin_hla",
    },
    "e88ddc776322b34b986bd5a06e3a9d59d7cc700e586f8d1ce7463a5b46aa89ce": {
        "name": "Yoon Me Me",
        "slug": "yoon_me_me",
    },
    "c82bdd4b0d456469690182efa69a949e38c85950fe9b693f996dbf08e7a98b06": {
        "name": "Khaing Thazin Nyein",
        "slug": "khaing_thazin_nyein",
    },
    "e43420fb85465bd13d3bd961dd97a020ff51371d384b2623fcc833d34a0bb397": {
        "name": "Hsu Myat Nandar",
        "slug": "hsu_myat_nandar",
    },
}

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


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.strip().lower().encode("utf-8")).hexdigest()


def authenticate_member() -> tuple[str, dict]:
    """Verify member using SHA-256 hash so plain-text keys never appear in GitHub."""
    # 1. Check if leader's private team_roster.py exists locally
    try:
        from core.team_roster import TEAM_MEMBERS
        roster_by_hash = {hash_key(k): v for k, v in TEAM_MEMBERS.items()}
    except ImportError:
        roster_by_hash = MEMBER_HASHES

    # 2. Check saved local login session
    if SESSION_FILE.exists():
        try:
            saved = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            saved_hash = saved.get("key_hash", "")
            if saved_hash in roster_by_hash:
                member = roster_by_hash[saved_hash]
                print(f"Welcome back, {member['name']}!")
                return saved_hash[:8], member
        except (json.JSONDecodeError, OSError):
            pass

    # 3. First-time login prompt
    while True:
        entered_key = input("Enter your unique Team Access Key: ").strip().lower()
        entered_hash = hash_key(entered_key)
        if entered_hash in roster_by_hash:
            member = roster_by_hash[entered_hash]
            SESSION_FILE.write_text(
                json.dumps({"key_hash": entered_hash}, indent=2),
                encoding="utf-8",
            )
            print(f"Verified! Logged in as {member['name']} (saved for future sessions).")
            return entered_hash[:8], member
        print("Invalid access key. Contact the team leader.")


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