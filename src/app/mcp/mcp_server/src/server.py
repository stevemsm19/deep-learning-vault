from mcp.server.fastmcp import FastMCP
from tools import register_tools
from logger import setup_logger

logger = setup_logger()


def create_server() -> FastMCP:
    mcp = FastMCP("Claude", json_response=True)

    register_tools(mcp)

    @mcp.tool()
    def health_check() -> str:
        logger.info("health_check called")
        return "ok"

    return mcp
