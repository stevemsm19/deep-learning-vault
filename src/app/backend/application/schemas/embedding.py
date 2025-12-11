from pydantic import BaseModel
from typing import List, Dict, Any


class EmbeddingsResponse(BaseModel):
    total_embeddings: int
    total_documents: int
    embedding_dimension: int
    embeddings: List[List[float]]
    metadatas: List[Dict[str, Any]]
