from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    num_results: int
    similarity_threshold: float


class ChatResponse(BaseModel):
    reply: str
