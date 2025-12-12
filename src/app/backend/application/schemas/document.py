from typing import List
from pydantic import BaseModel


class DocumentFileRequest(BaseModel):
    filename: str
    content: bytes


class AddDocumentsResponse(BaseModel):
    filenames: List[str]
    total_pages: int
    total_chunks: int
