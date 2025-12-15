from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from dataset import DATASET
from logger import setup_logger

logger = setup_logger()


def register_resources(mcp: FastMCP) -> None:

    @mcp.resource("image://{image_id}")
    def fetch_image(image_id: str) -> Optional[Dict[str, Any]]:
        logger.info("resource fetch image_id=%r", image_id)

        for item in DATASET:
            if item["id"] == image_id:
                return {
                    "id": item["id"],
                    "url": item["url"],
                    "description": item["description"],
                }

        logger.warning("missing image resource image_id=%r", image_id)
        return None
