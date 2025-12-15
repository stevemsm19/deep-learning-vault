from abc import ABC, abstractmethod
from typing import List, Dict, Union
from app.backend.domain.entities.document_entity import DocumentEntity


class IDocumentLoader(ABC):
    @abstractmethod
    async def load_documents(
        self, file_data: List[Dict[str, Union[bytes, str]]]
    ) -> List[DocumentEntity]:
        pass
