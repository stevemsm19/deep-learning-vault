from mcp.server.fastmcp import FastMCP
from logger import setup_logger

logger = setup_logger()


# def register_prompts(mcp: FastMCP) -> None:

#     @mcp.prompt()
#     def search_prompt(query: str) -> str:
#         prompt = f"""
#         Extract key visual search terms from: "{query}"
#         Then use search_images to find relevant images.
#         """
#         return prompt

#     @mcp.prompt()
#     def expand_query_prompt(query: str) -> str:
#         return f"""
#         The user asked: "{query}"

#         Task: Extract the financial concepts, keywords and categories relevant to this query.
#         Return them as a comma-separated list.
#         """
