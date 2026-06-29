import numpy as np
from sentence_transformers import SentenceTransformer


class InMemoryVectorStore:
    """Простое in-memory хранилище эмбеддингов."""

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.chunks: list[dict] = []
        self.embeddings: np.ndarray | None = None

    def build(self, chunks: list[dict]) -> None:
        """Строит эмбеддинги для чанков."""
        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]
        self.embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def search(self, query: str, top_k: int) -> list[dict]:
        """Ищет top-k близких чанков по cosine similarity."""
        query_embedding = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ query_embedding
        top_indexes = np.argsort(scores)[::-1][:top_k]

        results = []
        for index in top_indexes:
            chunk = self.chunks[int(index)]
            results.append(
                {
                    "doc_id": chunk["doc_id"],
                    "score": float(scores[index]),
                    "snippet": chunk["text"][:700],
                }
            )
        return results
