from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI

from app.backend.controllers.chat_controller import router as chat_router
from app.backend.controllers.detection_controller import router as detection_router
from app.backend.config.mcp import mcp_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await mcp_client.connect_to_server("src/app/mcp/mcp_server/src/main.py")
    print("MCP client initialized")

    yield

    await mcp_client.cleanup()
    print("MCP client disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(detection_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
