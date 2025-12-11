import httpx

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from logger import setup_logger

logger = setup_logger()


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def ask_financial_query(
        query: str, num_results: int, similarity_threshold: float
    ) -> Dict[str, Any]:
        logger.info("ask_financial_query query=%r", query)

        url = "http://localhost:8001/api/v1/semantic-search"

        payload = {
            "query": query,
            "num_results": num_results,
            "similarity_threshold": similarity_threshold,
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(url, json=payload)
                logger.info("payload=%r", payload)

            if response.status_code != 200:
                logger.error(
                    "API returned status %d: %s",
                    response.status_code,
                    response.text,
                )
                return {
                    "error": f"API returned status {response.status_code}",
                    "details": response.text,
                }

            data = response.json()

            logger.info("response=%r", data.get("context", ""))

            return {
                "context": data.get("context", ""),
                "raw_response": data,
            }

        except Exception as e:
            logger.exception("Error while calling legal API")
            return {"error": str(e)}
