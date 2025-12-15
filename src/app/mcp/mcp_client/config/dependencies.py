from fastapi import Request
import chromadb

from langchain_chroma import Chroma

from app.backend.application.services.document_service import DocumentService
from app.backend.application.services.embedding_service import EmbeddingService
from app.backend.application.services.search_service import SearchService
from app.backend.application.services.banknote_detection_service import (
    CashDetectionService,
)
from app.backend.config.settings import settings

from app.backend.infrastructure.persistence.chroma import ChromaRepository
from app.backend.infrastructure.persistence.document_loader import (
    DocumentLoaderRepository,
)
from app.backend.infrastructure.services.google_embedding import GoogleEmbedding
from app.backend.infrastructure.services.langchain_text_splitter import (
    RecursiveTextSplitter,
)
from app.backend.infrastructure.services.mcp_client import MCPChatClient
from app.backend.infrastructure.services.yolo_detector import YoloObjectDetector

from app.backend.utils.constants import CHUNK_OVERLAP, CHUNK_SIZE


yolo_implementation = YoloObjectDetector(model_path="./model/best.pt")


def get_detection_service() -> CashDetectionService:
    return CashDetectionService(detector=yolo_implementation)


def get_mcp_client(request: Request) -> MCPChatClient:
    return MCPChatClient(request.app.state.mcp_client)


def get_embeddings() -> GoogleEmbedding:
    return GoogleEmbedding(
        api_key=settings.google_api_key, model=settings.embedding_model
    )


def get_vector_store() -> Chroma:
    embeddings = get_embeddings()

    client = chromadb.HttpClient(host=settings.chroma_host, port=8000)

    client.get_or_create_collection(settings.collection_name)

    return Chroma(
        client=client,
        collection_name=settings.collection_name,
        embedding_function=embeddings,
    )


def get_document_service() -> DocumentService:
    vector_store = get_vector_store()

    document_loader_repository = DocumentLoaderRepository("/src/data/files")
    vector_store_repository = ChromaRepository(vector_store)

    text_splitter = RecursiveTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    return DocumentService(
        vector_store_repository=vector_store_repository,
        document_loader_repository=document_loader_repository,
        text_splitter=text_splitter,
    )


def get_search_service() -> SearchService:
    vector_store = get_vector_store()

    vector_store_repository = ChromaRepository(vector_store)

    return SearchService(vector_store_repository=vector_store_repository)


def get_embedding_service() -> EmbeddingService:
    vector_store = get_vector_store()

    vector_store_repository = ChromaRepository(vector_store)

    return EmbeddingService(vector_store_repository)
