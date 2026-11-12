import numpy as np


def normalize_landmarks(hand_landmarks) -> list[float]:
    """
    Convert 21 MediaPipe hand landmarks into a 63-element flat list (x, y, z)
    that is translation-invariant (centered on wrist) and scale-invariant.
    """
    coords = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks], dtype=np.float32)

    # 1. Center on Wrist (landmark index 0)
    wrist = coords[0].copy()
    coords -= wrist

    # 2. Scale by max Euclidean distance from wrist
    max_dist = np.max(np.linalg.norm(coords, axis=1))
    if max_dist > 0:
        coords /= max_dist

    return coords.flatten().tolist()