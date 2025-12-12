from abc import ABC, abstractmethod


class IChatClient(ABC):
    @abstractmethod
    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        document_names: str | None = None,
    ) -> str:
        pass
