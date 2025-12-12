import httpx

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from logger import setup_logger

logger = setup_logger()


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def ask_financial_query(
        query: str,
        num_results: int,
        similarity_threshold: float,
        document_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        logger.info("ask_financial_query query=%r", query)

        url = "http://localhost:8001/api/v1/semantic-search"

        payload = {
            "query": query,
            "num_results": num_results,
            "similarity_threshold": similarity_threshold,
        }

        if document_names:
            payload["document_names"] = document_names

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

            contents = [entity["content"] for entity in data["results"]]

            logger.info("total_results=%d", data["total_results"])

            return {
                "context": contents,
                "raw_response": data,
            }

        except Exception as e:
            logger.exception("Error while calling legal API")
            return {"error": str(e)}
