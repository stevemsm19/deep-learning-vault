import httpx

from typing import Any, Counter, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from logger import setup_logger

logger = setup_logger()


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def ask_financial_query(
        query: str,
        num_results: int,
        similarity_threshold: float,
        documents_name: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        logger.info("ask_financial_query query=%r", query)

        url = "http://localhost:8001/api/v1/semantic-search"

        payload = {
            "query": query,
            "num_results": num_results,
            "similarity_threshold": similarity_threshold,
        }

        if documents_name:
            payload["documents_name"] = documents_name

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

            sources = []
            seen_sources = set()
            for entity in data["results"]:
                source = entity["metadata"]["source"]
                page = entity["metadata"]["page"]
                source_key = f"{source}-{page}"

                if source_key not in seen_sources:
                    sources.append({"source": source, "page": page})
                    seen_sources.add(source_key)

            logger.info("total_results=%d", data["total_results"])

            return {
                "context": "\n\n".join(contents),
                "sources": sources,
                "raw_response": data,
            }

        except Exception as e:
            logger.exception("Error while calling financial API")
            return {"error": str(e)}

    @mcp.tool()
    async def count_bills(bills: List[str]) -> Dict[str, Any]:
        logger.info("count_bills called with %d bills", len(bills))

        bill_values = {
            "Cien_Mil": 100000,
            "Cincuenta_Mil": 50000,
            "Veinte_Mil": 20000,
            "Diez_Mil": 10000,
            "Cinco_Mil": 5000,
            "Dos_Mil": 2000,
        }

        invalid_bills = [b for b in bills if b not in bill_values]
        if invalid_bills:
            return {
                "error": f"Billetes inválidos encontrados: {invalid_bills}",
                "valid_bills": list(bill_values.keys()),
            }

        bill_count = Counter(bills)

        total = sum(bill_values[bill] * count for bill, count in bill_count.items())

        sorted_bills = sorted(
            bill_count.items(), key=lambda x: bill_values[x[0]], reverse=True
        )

        bill_summary = []
        for bill_name, count in sorted_bills:
            value = bill_values[bill_name]
            subtotal = value * count

            readable_name = bill_name.replace("_", " ")

            bill_summary.append(
                {
                    "denomination": readable_name,
                    "value": value,
                    "count": count,
                    "subtotal": subtotal,
                }
            )

        logger.info("Total counted: $%d from %d bills", total, len(bills))

        return {
            "success": True,
            "total_bills": len(bills),
            "total_amount": total,
            "bills_summary": bill_summary,
            "message": f"Se contaron {len(bills)} billetes por un total de ${total:,}",
        }
