from app.backend.domain.repositories.vector_store_repository import (
    IVectorStore,
)
from app.backend.domain.interfaces.llm_interface import ILLM

from app.backend.application.schemas.search import SearchRequest, SearchResponse


class SearchService:
    def __init__(self, vector_store_repository: IVectorStore):
        self.vector_store_repository = vector_store_repository

    async def search_and_answer(self, request: SearchRequest) -> SearchResponse:
        try:
            context_entities = await self.vector_store_repository.search_similar(
                request.question,
                request.num_results,
                request.similarity_threshold,
            )

            context_responses = []
            for entity in context_entities:
                context_responses.append(
                    {
                        "content": entity.content,
                        "metadata": entity.metadata,
                    }
                )

            context = "\n\n".join([entity.content for entity in context_entities])

            return SearchResponse(context=context)

        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
