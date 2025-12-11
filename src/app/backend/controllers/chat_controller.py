from fastapi import APIRouter, Depends

from app.backend.application.schemas.chat import ChatRequest, ChatResponse
from app.backend.config.dependencies import get_mcp_client
from app.backend.application.services.chat_service import ChatService
from app.backend.infrastructure.mcp_client import MCPChatClient


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    mcp_client: MCPChatClient = Depends(get_mcp_client),
) -> ChatResponse:
    service = ChatService(mcp_client)
    reply = await service.process_message(request.message)
    return ChatResponse(reply=reply)
