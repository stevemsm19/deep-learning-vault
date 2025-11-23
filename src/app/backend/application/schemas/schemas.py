from pydantic import BaseModel
from typing import List


class DetectionItem(BaseModel):
    category_name: str
    score: float
    x_min: float
    y_min: float
    width: float
    height: float


class DetectionResponse(BaseModel):
    filename: str
    detections: List[DetectionItem]
