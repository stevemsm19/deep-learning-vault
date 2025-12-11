import numpy as np

from typing import Any, Dict, List

from langchain_chroma import Chroma
from langchain_core.documents import Document as LangchainDocument

from app.backend.domain.repositories.vector_store_repository import (
    IVectorStore,
)
from app.backend.domain.entities.document_entity import DocumentEntity


class ChromaRepository(IVectorStore):
    def __init__(self, vector_store: Chroma):
        self.vector_store = vector_store

    async def add_document(self, documents: List[DocumentEntity]) -> List[str]:
        langchain_docs = [
            LangchainDocument(page_content=doc.content, metadata=doc.metadata)
            for doc in documents
        ]
        document_ids = self.vector_store.add_documents(documents=langchain_docs)
        return document_ids

    async def search_similar(
        self, query: str, num_results: int, similarity_threshold: float
    ) -> List[DocumentEntity]:

        results = self.vector_store.similarity_search_with_score(query, num_results)

        entities: List[DocumentEntity] = []
        for doc, score in results:
            if score <= similarity_threshold:

                entity = DocumentEntity(
                    content=doc.page_content, metadata={**doc.metadata, "score": score}
                )
                entities.append(entity)

        return entities

    async def get_embeddings(self) -> Dict[str, List[Any]]:
        data = self.vector_store.get(include=["embeddings", "metadatas"])

        embeddings = [np.array(e).tolist() for e in data["embeddings"]]
        metadatas = data["metadatas"]

        return {
            "embeddings": embeddings,
            "metadatas": metadatas,
        }
