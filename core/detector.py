from pathlib import Path
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20), # Pinky & Palm
]


class HandDetector:
    def __init__(self, model_path: str = "models/hand_landmarker.task", min_confidence: float = 0.6):
        resolved_path = str(Path(model_path).resolve())
        base_options = python.BaseOptions(model_asset_path=resolved_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=min_confidence,
            min_hand_presence_confidence=min_confidence,
            min_tracking_confidence=min_confidence,
            running_mode=vision.RunningMode.IMAGE,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def detect(self, bgr_frame):
        """Returns the first detected hand's 21 landmarks, or None if no hand is found."""
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.landmarker.detect(mp_image)

        if not result.hand_landmarks:
            return None
        return result.hand_landmarks[0]

    @staticmethod
    def draw_landmarks(bgr_frame, hand_landmarks):
        """Draws skeleton connections and landmark dots onto the frame in-place."""
        h, w, _ = bgr_frame.shape
        points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

        for start_idx, end_idx in HAND_CONNECTIONS:
            cv2.line(bgr_frame, points[start_idx], points[end_idx], (0, 255, 0), 2)

        for x, y in points:
            cv2.circle(bgr_frame, (x, y), 4, (0, 0, 255), -1)

        return bgr_frame