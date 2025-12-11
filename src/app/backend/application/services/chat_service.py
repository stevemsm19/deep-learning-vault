from app.backend.application.schemas.chat import ChatRequest, ChatResponse
from app.backend.domain.interfaces.chat_interface import IChatClient


class ChatService:
    def __init__(self, chat_client: IChatClient) -> None:
        self.chat_client = chat_client

    async def process_message(self, request: ChatRequest) -> str:
        return await self.chat_client.process_query(request.message)
