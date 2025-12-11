from abc import ABC, abstractmethod
from typing import List

from app.backend.domain.entities.detection_entity import DetectionResult


class IObjectDetector(ABC):
    @abstractmethod
    def process_image(
        self, image_bytes: bytes, conf: float, max_det: int
    ) -> List[DetectionResult]:
        pass
