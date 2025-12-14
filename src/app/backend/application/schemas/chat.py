from typing import List, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    num_results: int = 9
    similarity_threshold: float = 0.5
    documents_name: Optional[List[str]] = None
    bills: Optional[List[str]] = None


class ChatResponse(BaseModel):
    reply: str
