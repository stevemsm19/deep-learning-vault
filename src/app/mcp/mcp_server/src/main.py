from server import create_server
from logger import setup_logger

logger = setup_logger()


def main() -> None:
    logger.info("Starting MCP (stdio)")
    mcp = create_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
