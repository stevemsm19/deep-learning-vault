from typing import Dict, List, Union

from app.backend.domain.repositories.vector_store_repository import (
    IVectorStore,
)
from app.backend.domain.repositories.document_loader_repository import (
    IDocumentLoader,
)
from app.backend.domain.interfaces.text_splitter_interface import ITextSplitter

from app.backend.application.schemas.document import (
    DocumentFileRequest,
    AddDocumentsResponse,
)


class DocumentService:
    def __init__(
        self,
        vector_store_repository: IVectorStore,
        document_loader_repository: IDocumentLoader,
        text_splitter: ITextSplitter,
    ):
        self.vector_store_repository = vector_store_repository
        self.document_loader_repository = document_loader_repository
        self.text_splitter = text_splitter

    async def add_document_from_uploads(
        self, file: List[DocumentFileRequest]
    ) -> AddDocumentsResponse:
        try:

            file_data: List[Dict[str, Union[bytes, str]]] = [
                {"filename": dto.filename, "content": dto.content} for dto in file
            ]

            documents = await self.document_loader_repository.load_documents(file_data)

            chunks = self.text_splitter.split_documents(documents)

            await self.vector_store_repository.add_document(chunks)

            return AddDocumentsResponse(
                filenames=[dto.filename for dto in file],
                total_pages=len(documents),
                total_chunks=len(chunks),
            )
        except Exception as e:
            raise Exception(f"Error adding documents: {str(e)}")
