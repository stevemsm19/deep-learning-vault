from abc import ABC, abstractmethod


class IChatClient(ABC):
    @abstractmethod
    async def process_query(self, message: str) -> str:
        pass
