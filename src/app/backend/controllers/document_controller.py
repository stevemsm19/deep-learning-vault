from typing import List
from fastapi import HTTPException, UploadFile, File, APIRouter, Depends

from app.backend.application.services.document_service import DocumentService
from app.backend.application.schemas.document import (
    DocumentFileRequest,
    AddDocumentsResponse,
)

from app.backend.config.dependencies import get_document_service

router = APIRouter()


@router.post("/documents/add")
async def add_document(
    files: List[UploadFile] = File(...),
    document_service: DocumentService = Depends(get_document_service),
) -> AddDocumentsResponse:

    document_files = []
    for f in files:
        if f.filename is None:
            raise HTTPException(status_code=400, detail="File must have a filename")
        document_files.append(
            DocumentFileRequest(filename=f.filename, content=await f.read())
        )

    result_dto = await document_service.add_document_from_uploads(document_files)

    return AddDocumentsResponse(
        total_pages=result_dto.total_pages, total_chunks=result_dto.total_chunks
    )
