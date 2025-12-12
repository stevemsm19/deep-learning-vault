from typing import List, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    num_results: int
    similarity_threshold: float
    document_names: Optional[List[str]] = None


class ChatResponse(BaseModel):
    reply: str
