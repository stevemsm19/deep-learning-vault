from app.backend.domain.interfaces.chat_interface import IChatClient
from app.mcp.mcp_client.client import MCPClient as RealMCPClient


class MCPChatClient(IChatClient):
    def __init__(self, mcp_client: RealMCPClient) -> None:
        self.mcp_client = mcp_client

    async def process_query(self, message: str) -> str:
        return await self.mcp_client.process_query(message)
