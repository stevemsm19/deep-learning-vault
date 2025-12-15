from abc import ABC, abstractmethod
from typing import List


class IChatClient(ABC):
    @abstractmethod
    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: List[str] | None = None,
        bills: List[str] | None = None,
    ) -> str:
        pass
