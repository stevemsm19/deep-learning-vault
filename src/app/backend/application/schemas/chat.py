from typing import List, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    num_results: int
    similarity_threshold: float
    documents_name: Optional[List[str]] = None


class ChatResponse(BaseModel):
    reply: str
