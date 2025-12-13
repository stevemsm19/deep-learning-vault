from app.backend.domain.interfaces.chat_interface import IChatClient
from app.mcp.mcp_client.client import MCPClient


class MCPChatClient(IChatClient):
    def __init__(self, mcp_client: MCPClient) -> None:
        self.mcp_client = mcp_client

    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: str | None = None,
    ) -> str:
        return await self.mcp_client.process_query(
            query, num_results, similarity_threshold, documents_name
        )
