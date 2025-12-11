from typing import List, cast
from google import genai

from langchain_core.embeddings import Embeddings


class GoogleEmbedding(Embeddings):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), 100):
            batch = texts[i : i + 100]

            response = self.client.models.embed_content(
                model=self.model, contents=batch  # type: ignore [arg-type]
            )

            if not response.embeddings:
                continue

            for e in response.embeddings:
                embedding = cast(List[float], e.values or [])
                all_embeddings.append(embedding)

        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        response = self.client.models.embed_content(model=self.model, contents=text)
        if not response.embeddings:
            return []
        embedding = cast(List[float], response.embeddings[0].values or [])
        return embedding
