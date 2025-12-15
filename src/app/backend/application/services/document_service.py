from pathlib import Path
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

    async def get_documents_name(self) -> List[str]:
        try:
            data = await self.vector_store_repository.get_sources()
            names = []
            seen = set()
            for name in data:
                if name and name not in seen:
                    seen.add(name)
                    names.append(name)

            return names
        except Exception as e:
            raise Exception(f"Error getting documents names: {str(e)}")


async def load_initial_documents(
    document_service: DocumentService,
    files_dir: Path,
) -> None:
    existing_names = await document_service.get_documents_name()

    if existing_names:
        print(f"Documentos ya cargados ({len(existing_names)})")
        return

    if not files_dir.exists():
        print("Carpeta de documentos iniciales no existe")
        return

    documents: List[DocumentFileRequest] = []

    for file_path in files_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".pdf":
            documents.append(
                DocumentFileRequest(
                    filename=file_path.name,
                    content=file_path.read_bytes(),
                )
            )

    if not documents:
        print("No hay documentos para cargar")
        return

    print(f"Cargando {len(documents)} documentos iniciales...")

    await document_service.add_document_from_uploads(documents)

    print("Documentos iniciales cargados correctamente")
