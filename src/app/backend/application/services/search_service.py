from typing import List
from app.backend.domain.repositories.vector_store_repository import (
    IVectorStore,
)

from app.backend.application.schemas.search import (
    DocumentMetadata,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


class SearchService:
    def __init__(self, vector_store_repository: IVectorStore):
        self.vector_store_repository = vector_store_repository

    async def search(self, request: SearchRequest) -> SearchResponse:
        try:
            context_entities = await self.vector_store_repository.search_similar(
                request.query,
                request.num_results,
                request.similarity_threshold,
                request.documents_name,
            )

            context_responses: List[SearchResult] = []
            for entity in context_entities:
                context_responses.append(
                    SearchResult(
                        content=entity.content,
                        metadata=DocumentMetadata(
                            source=entity.metadata.get("source") or "",
                            page=entity.metadata.get("page") or 0,
                            score=entity.metadata.get("score") or None,
                        ),
                    )
                )

            return SearchResponse(
                query=request.query,
                total_results=len(context_responses),
                results=context_responses,
            )

        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
