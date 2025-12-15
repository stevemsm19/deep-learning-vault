from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class SearchRequest(BaseModel):
    query: str
    num_results: int
    similarity_threshold: float
    documents_name: Optional[List[str]] = None


class DocumentMetadata(BaseModel):
    source: str
    page: int
    score: Optional[float]


class SearchResult(BaseModel):
    content: str
    metadata: DocumentMetadata


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResult]
