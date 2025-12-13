from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.backend.domain.entities.document_entity import DocumentEntity


class IVectorStore(ABC):
    @abstractmethod
    async def add_document(self, documents: List[DocumentEntity]) -> List[str]:
        pass

    @abstractmethod
    async def search_similar(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        document_names: List[str] = None,
    ) -> List[DocumentEntity]:
        pass

    @abstractmethod
    async def get_embeddings(self) -> Dict[str, List[Any]]:
        pass

    @abstractmethod
    async def get_sources(self) -> List[str]:
        pass
