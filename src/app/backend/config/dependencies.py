from fastapi import HTTPException

from app.backend.config.mcp import mcp_client

from app.backend.application.services.banknote_detection_service import (
    CashDetectionService,
)
from app.backend.infrastructure.yolo_detector import YoloService
from app.mcp.mcp_client.client import MCPClient

yolo_implementation = YoloService(model_path="./model/best.pt")


def get_detection_service() -> CashDetectionService:
    return CashDetectionService(detector=yolo_implementation)


def get_mcp_client() -> MCPClient:
    if mcp_client is None or mcp_client.session is None:
        raise HTTPException(status_code=500, detail="MCP client not initialized")
    return mcp_client
