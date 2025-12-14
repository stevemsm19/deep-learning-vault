from typing import List, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path

from app.mcp.mcp_client.prompts import build_system_prompt

load_dotenv()  # load environment variables from .env

# Claude model constant
ANTHROPIC_MODEL = "claude-3-haiku-20240307"


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        if is_python:
            path = Path(server_script_path).resolve()
            server_params = StdioServerParameters(
                command="uv",
                args=["--directory", str(path.parent), "run", path.name],
                env=None,
            )
        else:
            server_params = StdioServerParameters(
                command="node", args=[server_script_path], env=None
            )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(
        self,
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: Optional[List[str]] = None,
        bills: Optional[List[str]] = None,
    ) -> str:
        """Process a query using Claude and available tools

        Args:
            query: The user's query
            num_results: Number of results for semantic search
            similarity_threshold: Minimum similarity threshold
            documents_name: Optional document name to filter results
        """

        system_prompt = build_system_prompt(
            query=query,
            num_results=num_results,
            similarity_threshold=similarity_threshold,
            documents_name=documents_name,
            bills=bills,
        )

        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
            system=system_prompt,
        )

        while response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    # Execute tool call
                    result = await self.session.call_tool(content.name, content.input)

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content,
                        }
                    )

            messages.append({"role": "user", "content": tool_results})

            # Get next response from Claude
            response = self.anthropic.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=1000,
                messages=messages,
                tools=available_tools,
                system=system_prompt,
            )

        final_text = []
        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)

        return "\n".join(final_text)

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
