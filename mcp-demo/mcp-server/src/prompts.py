from mcp.server.fastmcp import FastMCP
from logger import setup_logger

logger = setup_logger()


def register_prompts(mcp: FastMCP) -> None:

    @mcp.prompt()
    def search_prompt(query: str) -> str:
        prompt = f"""
        Extract key visual search terms from: "{query}"
        Then use search_images to find relevant images.
        """
        return prompt

    @mcp.prompt()
    def description_prompt(image_id: str) -> str:
        prompt = f"""
        Use get_image_description to retrieve details about image: {image_id}
        """
        return prompt
