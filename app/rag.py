from app.config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR, EMBEDDING_MODEL_NAME, TOP_K
from app.document_loader import load_documents
from app.llm import call_llm
from app.prompting import build_prompt
from app.text_splitter import build_chunks
from app.vector_store import InMemoryVectorStore


class RAGPipeline:
    """RAG-пайплайн: документы -> чанки -> эмбеддинги -> поиск -> ответ."""

    def __init__(self):
        self.documents = []
        self.chunks = []
        self.vector_store = InMemoryVectorStore(EMBEDDING_MODEL_NAME)

    def build_index(self) -> None:
        """Загружает документы и строит индекс."""
        self.documents = load_documents(DOCS_DIR)
        self.chunks = build_chunks(self.documents, CHUNK_SIZE, CHUNK_OVERLAP)
        self.vector_store.build(self.chunks)

    def ask(self, question: str, top_k: int = TOP_K) -> dict:
        """Ищет источники и получает ответ LLM."""
        sources = self.vector_store.search(question, top_k)
        messages = build_prompt(question, sources)
        answer = call_llm(messages)
        return {"answer": answer, "sources": sources}
