import re
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangchainDocument

from app.backend.domain.entities.document_entity import DocumentEntity
from app.backend.domain.interfaces.text_splitter_interface import ITextSplitter


class RecursiveTextSplitter(ITextSplitter):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def __clean_text(self, text: str) -> str:
        text = re.sub(r"\n+", "\n", text)
        text = re.sub(r"\t+", " ", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = text.strip()

        return text

    def __split_by_sections(self, doc: LangchainDocument) -> List[LangchainDocument]:
        text = self.__clean_text(doc.page_content)

        parts = text.split("\n\n")
        valid_parts = [p.strip() for p in parts if len(p.strip()) > 0]

        split_sections = []
        for part in valid_parts:
            split_sections.append(
                LangchainDocument(page_content=part, metadata=doc.metadata)
            )

        return split_sections

    def split_documents(self, documents: List[DocumentEntity]) -> List[DocumentEntity]:
        langchain_docs = [
            LangchainDocument(page_content=doc.content, metadata=doc.metadata)
            for doc in documents
        ]

        structured_docs = []
        for doc in langchain_docs:
            structured_docs.extend(self.__split_by_sections(doc))

        split_langchain_docs = []
        for doc in structured_docs:
            if len(doc.page_content) > self.text_splitter._chunk_size:
                sub_chunks = self.text_splitter.split_documents([doc])
                split_langchain_docs.extend(sub_chunks)
            else:
                split_langchain_docs.append(doc)

        return [
            DocumentEntity(content=doc.page_content, metadata=doc.metadata)
            for doc in split_langchain_docs
        ]
