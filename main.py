import logging

from fastapi import FastAPI, HTTPException

from app.rag import RAGPipeline
from app.schemas import AskRequest, AskResponse, HealthResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-service")

app = FastAPI(
    title="IB Documents RAG Service",
    description="Backend-сервис для ответов на вопросы по документам информационной безопасности",
    version="1.0.0",
)

rag = RAGPipeline()


@app.on_event("startup")
def startup_event():
    """Строит индекс при запуске сервиса."""
    logger.info("Building RAG index...")
    rag.build_index()
    logger.info("Loaded %s documents and %s chunks", len(rag.documents), len(rag.chunks))


@app.get("/health", response_model=HealthResponse)
def health():
    """Проверка статуса сервиса."""
    return {
        "status": "ok",
        "documents": len(rag.documents),
        "chunks": len(rag.chunks),
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """Ответ на вопрос пользователя."""
    logger.info("Question: %s", request.question)

    try:
        result = rag.ask(request.question)
        return result
    except Exception as error:
        logger.exception("RAG error")
        raise HTTPException(status_code=500, detail=str(error)) from error
