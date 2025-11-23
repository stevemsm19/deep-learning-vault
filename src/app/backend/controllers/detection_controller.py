from fastapi import APIRouter, Form, UploadFile, File, Depends
from typing import List

from app.backend.application.schemas.schemas import DetectionResponse
from app.backend.application.services.impl.banknote_detection_service import (
    CashDetectionService,
)
from app.backend.config.dependencies import get_detection_service

router = APIRouter()


@router.post("/predict")
async def predict(
    files: List[UploadFile] = File(...),
    conf: float = Form(0.8),
    max_det: int = Form(1),
    service: CashDetectionService = Depends(get_detection_service),
) -> List[DetectionResponse]:
    results = []
    for file in files:
        content = await file.read()
        response = service.detect_objects(
            file.filename or "unknown", content, conf, max_det
        )
        results.append(response)
    return results
