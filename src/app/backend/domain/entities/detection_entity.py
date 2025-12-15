from dataclasses import dataclass


@dataclass
class DetectionResult:
    category_name: str
    score: float
    x_min: float
    y_min: float
    width: float
    height: float
