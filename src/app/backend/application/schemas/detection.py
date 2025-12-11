from fastapi import UploadFile
from pydantic import BaseModel
from typing import List

from app.backend.domain.entities.detection_entity import DetectionResult


class DetectionResponse(BaseModel):
    filename: str
    detections: List[DetectionResult]
