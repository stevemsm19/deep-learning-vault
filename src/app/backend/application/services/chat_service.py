from app.backend.application.schemas.chat import ChatRequest, ChatResponse
from app.backend.domain.interfaces.chat_interface import IChatClient


class ChatService:
    def __init__(self, chat_client: IChatClient) -> None:
        self.chat_client = chat_client

    async def process_query(self, request: ChatRequest) -> str:
        return await self.chat_client.process_query(
            query=request.query,
            num_results=request.num_results,
            similarity_threshold=request.similarity_threshold,
        )
