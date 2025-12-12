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

    async def search_and_answer(self, request: SearchRequest) -> SearchResponse:
        try:
            context_entities = await self.vector_store_repository.search_similar(
                request.query,
                request.num_results,
                request.similarity_threshold,
            )

            if request.document_name:
                filtered_entities = [
                    e
                    for e in context_entities
                    if (e.metadata or {}).get("source") == request.document_name
                ]
            else:
                filtered_entities = context_entities

            context_responses: List[SearchResult] = []
            for entity in filtered_entities:
                context_responses.append(
                    SearchResult(
                        content=entity.content,
                        metadata=DocumentMetadata(
                            source=entity.metadata.get("source"),
                            page=entity.metadata.get("page"),
                            score=entity.metadata.get("score"),
                        ),
                    )
                )

            context = "\n\n".join([entity.content for entity in filtered_entities])

            return SearchResponse(
                query=request.query,
                total_results=len(filtered_entities),
                results=context_responses,
            )

        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
