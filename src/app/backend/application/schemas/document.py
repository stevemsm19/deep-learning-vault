from pydantic import BaseModel


class DocumentFileRequest(BaseModel):
    filename: str
    content: bytes


class AddDocumentsResponse(BaseModel):
    total_pages: int
    total_chunks: int
