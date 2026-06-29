def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Режет текст на чанки с перекрытием."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap

    return chunks


def build_chunks(documents: list[dict], chunk_size: int, chunk_overlap: int) -> list[dict]:
    """Создает чанки для всех документов."""
    chunks = []
    for document in documents:
        doc_chunks = split_text(document["text"], chunk_size, chunk_overlap)
        for i, chunk_text in enumerate(doc_chunks):
            chunks.append(
                {
                    "chunk_id": f'{document["doc_id"]}_{i}',
                    "doc_id": document["doc_id"],
                    "path": document["path"],
                    "text": chunk_text,
                }
            )
    return chunks
