from abc import ABC, abstractmethod


class IChatClient(ABC):
    @abstractmethod
    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: str | None = None,
        bills: list | None = None,
    ) -> str:
        pass
