from abc import ABC, abstractmethod
from typing import List
from app.backend.application.schemas.schemas import DetectionItem


class IObjectDetector(ABC):
    @abstractmethod
    def process_image(
        self, image_bytes: bytes, conf: float, max_det: int
    ) -> List[DetectionItem]:
        pass
