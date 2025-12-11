from fastapi import APIRouter, Depends

from app.backend.application.schemas.embedding import EmbeddingsResponse
from app.backend.application.services.embedding_service import EmbeddingService

from app.backend.config.dependencies import get_embedding_service

router = APIRouter()


@router.get("/embeddings")
async def get_embeddings(
    limit: int | None = None,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> EmbeddingsResponse:

    data = await embedding_service.get_embeddings()
    embeddings = data["embeddings"]
    metadatas = data["metadatas"]

    total_embeddings = len(embeddings)
    total_documents = len({m["source"] for m in metadatas})
    dim = len(embeddings[0]) if total_embeddings > 0 else 0

    if limit is not None:
        embeddings = embeddings[:limit]
        metadatas = metadatas[:limit]

    return EmbeddingsResponse(
        total_embeddings=total_embeddings,
        total_documents=total_documents,
        embedding_dimension=dim,
        embeddings=embeddings,
        metadatas=metadatas,
    )
