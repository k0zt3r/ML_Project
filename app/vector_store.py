import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import HashingVectorizer


class InMemoryVectorStore:
    """Простое in-memory хранилище эмбеддингов."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.vectorizer = None
        self.backend = "sentence-transformers"
        self.chunks: list[dict] = []
        self.embeddings = None

    def build(self, chunks: list[dict]) -> None:
        """Строит эмбеддинги для чанков."""
        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]

        try:
            self.model = SentenceTransformer(self.model_name)
            self.embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=True,
            )
            self.backend = "sentence-transformers"
        except Exception as error:
            print("SentenceTransformer не загрузился, использую HashingVectorizer.")
            print("Ошибка:", error)
            self.vectorizer = HashingVectorizer(
                n_features=4096,
                norm="l2",
                alternate_sign=False,
            )
            self.embeddings = self.vectorizer.transform(texts)
            self.backend = "hashing-vectorizer"

    def search(self, query: str, top_k: int) -> list[dict]:
        """Ищет top-k близких чанков по cosine similarity."""
        if self.backend == "sentence-transformers":
            query_embedding = self.model.encode([query], normalize_embeddings=True)[0]
            scores = self.embeddings @ query_embedding
        else:
            query_embedding = self.vectorizer.transform([query])
            scores = (self.embeddings @ query_embedding.T).toarray().ravel()

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
