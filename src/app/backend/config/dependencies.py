from app.backend.application.services.impl.banknote_detection_service import (
    CashDetectionService,
)
from app.backend.infrastructure.yolo_detector import YoloService

yolo_implementation = YoloService(model_path="./model/best.pt")


def get_detection_service() -> CashDetectionService:
    return CashDetectionService(detector=yolo_implementation)
