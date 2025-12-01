import asyncio
import sys
import os
from typing import Optional, Dict, Any, Tuple
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import google.generativeai as genai  # type: ignore
from google.ai.generativelanguage import Content, Part, FunctionResponse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"


class MCPClient:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)

    async def connect_to_server(self, server_script_path: str) -> None:
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

        if self.session is None:
            raise RuntimeError("Session not initialized")

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    def _convert_tool_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        type_map: Dict[str, str] = {
            "string": "STRING",
            "number": "NUMBER",
            "integer": "INTEGER",
            "boolean": "BOOLEAN",
            "array": "ARRAY",
            "object": "OBJECT",
        }

        result: Dict[str, Any] = {}
        if "type" in schema:
            result["type"] = type_map.get(schema["type"], "STRING")
        if "description" in schema:
            result["description"] = schema["description"]
        if "properties" in schema:
            result["properties"] = {
                k: self._convert_tool_schema(v) for k, v in schema["properties"].items()
            }
        if "required" in schema:
            result["required"] = schema["required"]
        if "items" in schema:
            result["items"] = self._convert_tool_schema(schema["items"])
        return result

    def _detect_query_type(self, query: str) -> Tuple[str, Dict[str, str]]:
        query_lower = query.lower()

        if any(
            word in query_lower
            for word in ["describe", "description", "details", "img-", "image id"]
        ):
            import re

            match = re.search(r"img-\d+", query)
            if match:
                return "description_prompt", {"image_id": match.group()}

        return "search_prompt", {"query": query}

    async def process_query(self, query: str) -> str:
        if self.session is None:
            raise RuntimeError("Session not initialized")

        response = await self.session.list_tools()

        gemini_tools = []
        for tool in response.tools:
            gemini_tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": self._convert_tool_schema(tool.inputSchema),
                }
            )

        model = genai.GenerativeModel(model_name=GEMINI_MODEL, tools=gemini_tools)
        chat = model.start_chat(enable_automatic_function_calling=False)

        response = chat.send_message(query)
        final_text = []

        for _ in range(10):
            for part in response.parts:
                if hasattr(part, "text") and part.text:
                    final_text.append(part.text)

                elif hasattr(part, "function_call") and part.function_call:
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    result = await self.session.call_tool(tool_name, tool_args)
                    final_text.append(
                        f"[Calling tool {tool_name} with args {tool_args}]"
                    )

                    if result.content:
                        if isinstance(result.content, list):
                            tool_output = "\n".join(
                                item.text if hasattr(item, "text") else str(item)
                                for item in result.content
                            )
                        else:
                            tool_output = (
                                result.content.text
                                if hasattr(result.content, "text")
                                else str(result.content)
                            )
                    else:
                        tool_output = str(result)

                    function_response = Part(
                        function_response=FunctionResponse(
                            name=tool_name, response={"result": tool_output}
                        )
                    )

                    response = chat.send_message(Content(parts=[function_response]))
                    break
            else:
                break

        return "\n".join(final_text)

    async def chat_loop(self) -> None:
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self) -> None:
        await self.exit_stack.aclose()


async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
