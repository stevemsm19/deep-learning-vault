from typing import List, Optional, Any, Tuple
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic

from app.mcp.mcp_client.config.settings import Settings
from app.mcp.mcp_client.prompts import build_system_prompt

ANTHROPIC_MODEL = "claude-3-haiku-20240307"

settings = Settings()


class MCPClient:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        self.anthropic: Anthropic = Anthropic(api_key=settings.anthropic_api_key)

        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, server_script_path: str) -> None:
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        if is_python:
            path = Path(server_script_path).resolve()
            server_params = StdioServerParameters(
                command="python",
                args=[str(path)],
                env=None,
            )
        else:
            server_params = StdioServerParameters(
                command="node",
                args=[server_script_path],
                env=None,
            )

        self.stdio, self.write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        response = await self.session.list_tools()
        print(
            "\nConnected to server with tools:", [tool.name for tool in response.tools]
        )

    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: Optional[List[str]] = None,
        bills: Optional[List[str]] = None,
    ) -> str:
        system_prompt = build_system_prompt(
            query=query,
            num_results=num_results,
            similarity_threshold=similarity_threshold,
            documents_name=documents_name,
            bills=bills,
        )

        messages: List[dict[str, Any]] = [{"role": "user", "content": query}]

        response = await self.session.list_tools()  # type: ignore[union-attr]

        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        response = self.anthropic.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
            system=system_prompt,
        )

        while response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results: List[dict[str, Any]] = []
            for content in response.content:
                if content.type == "tool_use":
                    result = await self.session.call_tool(  # type: ignore[union-attr]
                        content.name, content.input
                    )
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content,
                        }
                    )

            messages.append({"role": "user", "content": tool_results})

            response = self.anthropic.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=1000,
                messages=messages,
                tools=available_tools,
                system=system_prompt,
            )

        final_text: List[str] = [
            content.text for content in response.content if content.type == "text"
        ]

        return "\n".join(final_text)

    async def cleanup(self) -> None:
        await self.exit_stack.aclose()
