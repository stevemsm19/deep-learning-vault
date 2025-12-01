from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from dataset import DATASET
from logger import setup_logger

logger = setup_logger()


def _text_score(text: str, query: str) -> int:
    text_l = text.lower()
    q = query.lower()
    score = 0

    if q in text_l:
        score += 50

    for token in q.split():
        if token in text_l:
            score += 10

    return score


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def search_images(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info("search_images query=%r top_k=%d", query, top_k)

        results = []
        for item in DATASET:
            score_desc = _text_score(item["description"], query)
            score_tags = sum(_text_score(t, query) for t in item["tags"])
            score = score_desc + score_tags

            if score > 0:
                results.append(
                    {
                        "id": item["id"],
                        "url": item["url"],
                        "description": item["description"],
                        "score": score,
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @mcp.tool()
    def get_image_description(image_id: str) -> Optional[str]:
        logger.info("get_image_description image_id=%r", image_id)

        for item in DATASET:
            if item["id"] == image_id:
                return str(item["description"])

        logger.warning("image_id=%r not found", image_id)
        return None
