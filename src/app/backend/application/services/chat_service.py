from app.mcp.mcp_client.client import MCPClient


class ChatService:
    def __init__(self, mcp_client: MCPClient) -> None:
        self.mcp_client = mcp_client

    async def process_message(self, message: str) -> str:
        reply: str = await self.mcp_client.process_query(message)
        return reply
