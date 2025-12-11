from fastapi import APIRouter, Depends

from app.backend.application.services.search_service import SearchService
from app.backend.application.schemas.search import SearchRequest, SearchResponse

from app.backend.config.dependencies import get_search_service

router = APIRouter()


@router.post("/semantic-search")
async def semantic_search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:

    request = SearchRequest(
        query=request.query,
        num_results=request.num_results,
        similarity_threshold=request.similarity_threshold,
    )

    result = await search_service.search_and_answer(request)

    return SearchResponse(
        context=result.context,
    )
