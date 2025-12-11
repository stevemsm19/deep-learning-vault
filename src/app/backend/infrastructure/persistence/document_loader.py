import os
import pymupdf

from typing import Dict, List, Union, cast

from fastapi import HTTPException

from app.backend.domain.repositories.document_loader_repository import (
    IDocumentLoader,
)
from app.backend.domain.entities.document_entity import DocumentEntity


class DocumentLoaderRepository(IDocumentLoader):
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir

    def __save_file(self, filename: str, content: bytes) -> str:
        if not filename:
            raise HTTPException(
                status_code=400, detail="Uploaded file must have a filename"
            )

        try:
            os.makedirs(self.upload_dir, exist_ok=True)
            file_path = os.path.join(self.upload_dir, filename)

            with open(file_path, "wb") as f:
                f.write(content)

            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    async def __load_pdf(self, file_path: str) -> List[DocumentEntity]:
        entities: List[DocumentEntity] = []

        try:
            pdf = pymupdf.open(file_path)
            for i, page in enumerate(pdf):
                text = page.get_text("text")
                if not text:
                    continue

                relative_source = (
                    file_path.split("temp_files/")[-1]
                    if "temp_files/" in file_path
                    else file_path
                )

                entity = DocumentEntity(
                    content=text, metadata={"source": relative_source, "page": i + 1}
                )
                entities.append(entity)

            return entities

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading PDF: {str(e)}")

    def __load_txt(self, file_path: str) -> List[DocumentEntity]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            entity = DocumentEntity(content=content, metadata={"source": file_path})
            return [entity]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading TXT: {str(e)}")

    async def load_documents(
        self, file_data: List[Dict[str, Union[bytes, str]]]
    ) -> List[DocumentEntity]:
        saved_file_paths = []
        for file_info in file_data:
            filename = cast(str, file_info["filename"])
            content = cast(bytes, file_info["content"])
            file_path = self.__save_file(filename, content)
            saved_file_paths.append(file_path)

        entities: List[DocumentEntity] = []
        for file_path in saved_file_paths:
            if file_path.endswith(".pdf"):
                docs = await self.__load_pdf(file_path)
            elif file_path.endswith(".txt"):
                docs = self.__load_txt(file_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")

            entities.extend(docs)

        return entities
