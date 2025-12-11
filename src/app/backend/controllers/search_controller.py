from fastapi import APIRouter, Depends

from app.backend.application.services.search_service import SearchService
from app.backend.application.schemas.search import SearchRequest, SearchResponse

from app.backend.config.dependencies import get_search_service

router = APIRouter()


@router.post("/semantic-search")
async def ask_question(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:

    request_dto = SearchRequest(
        question=request.question,
        num_results=request.num_results,
        similarity_threshold=request.similarity_threshold,
    )

    result = await search_service.search_and_answer(request_dto)

    return SearchResponse(
        context=result.context,
    )
