from fastapi import UploadFile
from pydantic import BaseModel
from typing import List

from app.backend.domain.entities.detection_entity import DetectionResult


class DetectionRequest(BaseModel):
    files: List[UploadFile]
    conf: float = 0.8
    max_det: int = 1


class DetectionResponse(BaseModel):
    filename: str
    detections: List[DetectionResult]
