from typing import List
from ultralytics import YOLO  # type: ignore[attr-defined]
from PIL import Image
import io

from app.backend.domain.entities.detection_entity import DetectionResult
from app.backend.domain.interfaces.banknote_detection_interface import IObjectDetector


class YoloObjectDetector(IObjectDetector):
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def process_image(
        self, image_bytes: bytes, conf: float, max_det: int
    ) -> List[DetectionResult]:
        image = Image.open(io.BytesIO(image_bytes))
        results = self.model(image, conf=conf, max_det=max_det, verbose=False)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detection = DetectionResult(
                    category_name=result.names[int(box.cls[0])],
                    score=float(box.conf[0]),
                    x_min=x1,
                    y_min=y1,
                    width=x2 - x1,
                    height=y2 - y1,
                )
                detections.append(detection)
        return detections
