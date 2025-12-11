from typing import Any, Dict, List

from app.backend.domain.repositories.vector_store_repository import (
    IVectorStore,
)


class EmbeddingService:
    def __init__(
        self,
        vector_store_repository: IVectorStore,
    ):
        self.vector_store_repository = vector_store_repository

    async def get_embeddings(self) -> Dict[str, List[Any]]:
        try:
            return await self.vector_store_repository.get_embeddings()
        except Exception as e:
            raise Exception(f"Error getting embeddings: {str(e)}")
