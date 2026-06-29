from pydantic import BaseModel, Field

from app.config import MAX_QUESTION_LENGTH


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=MAX_QUESTION_LENGTH)


class Source(BaseModel):
    doc_id: str
    score: float
    snippet: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class HealthResponse(BaseModel):
    status: str
    documents: int
    chunks: int
    vector_backend: str
