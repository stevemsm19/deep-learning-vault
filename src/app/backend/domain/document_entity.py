from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DocumentEntity:
    content: str
    metadata: Dict[str, Any]
