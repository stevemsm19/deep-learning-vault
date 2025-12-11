from pydantic import BaseModel
from typing import List, Dict, Any


class SearchRequest(BaseModel):
    question: str
    num_results: int
    similarity_threshold: float


class SearchResponse(BaseModel):
    context: str
