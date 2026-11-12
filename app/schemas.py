from pydantic import BaseModel, Field


class LandmarkRequest(BaseModel):
    landmarks: list[float] = Field(
        ...,
        min_length=63,
        max_length=63,
        description="63 normalized wrist-relative hand landmark coordinates (x0, y0, z0 ... x20, y20, z20)",
    )


class PredictionResponse(BaseModel):
    hand_detected: bool
    label_id: str | None = None
    myanmar_char: str | None = None
    confidence: float | None = None
    probabilities: dict[str, float] | None = None