from typing import List
from fastapi import HTTPException, UploadFile, File, APIRouter, Depends

from app.backend.application.services.document_service import DocumentService
from app.backend.application.schemas.document import (
    DocumentFileRequest,
    AddDocumentsResponse,
    DocumentNamesResponse,
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

    result = await document_service.add_document_from_uploads(document_files)

    return AddDocumentsResponse(
        filenames=result.filenames,
        total_pages=result.total_pages,
        total_chunks=result.total_chunks,
    )


@router.get("/documents/names", response_model=DocumentNamesResponse)
async def get_documents_name(
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentNamesResponse:
    names = await document_service.get_documents_name()
    return DocumentNamesResponse(names=names)
