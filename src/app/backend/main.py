from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI

from app.backend.application.services.document_service import load_initial_documents
from app.backend.config.dependencies import get_document_service
from app.backend.controllers.chat_controller import router as chat_router
from app.backend.controllers.detection_controller import router as detection_router
from app.mcp.mcp_client.client import MCPClient

from app.backend.controllers.document_controller import (
    router as document_router,
)
from app.backend.controllers.search_controller import (
    router as search_router,
)
from app.backend.controllers.embeddings_controller import (
    router as embedding_router,
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

MCP_SERVER_PATH = BASE_DIR / "src" / "app" / "mcp" / "mcp_server" / "src" / "main.py"
FILES_PATH = BASE_DIR / "src" / "data" / "files"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    mcp_client = MCPClient()
    await mcp_client.connect_to_server(str(MCP_SERVER_PATH))
    print("MCP client initialized")

    app.state.mcp_client = mcp_client

    document_service = get_document_service()
    await load_initial_documents(document_service, FILES_PATH)

    yield

    await mcp_client.cleanup()
    print("MCP client disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(detection_router, prefix="/api/v1")
app.include_router(document_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(embedding_router, prefix="/api/v1")
