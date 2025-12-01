from app.backend.domain.interfaces.banknote_detection_interface import IObjectDetector

from app.backend.application.schemas.schemas import DetectionResponse


class CashDetectionService:

    def __init__(self, detector: IObjectDetector):
        self.detector = detector

    def detect_objects(
        self, filename: str, image_bytes: bytes, conf: float, max_det: int
    ) -> DetectionResponse:
        detections = self.detector.process_image(
            image_bytes, conf=conf, max_det=max_det
        )

        return DetectionResponse(filename=filename, detections=detections)
