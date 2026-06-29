SYSTEM_PROMPT = """Ты помощник по документам в области информационной безопасности.
Отвечай только на основе найденного контекста.
Если в контексте нет ответа, скажи: "Информации в документах недостаточно".
Не выдумывай факты и не ссылайся на документы, которых нет в контексте."""


def build_prompt(question: str, sources: list[dict]) -> list[dict]:
    """Собирает сообщения для LLM."""
    context_parts = []
    for i, source in enumerate(sources, start=1):
        context_parts.append(
            f"[Источник {i}: {source['doc_id']}, score={source['score']:.3f}]\n"
            f"{source['snippet']}"
        )

    context = "\n\n".join(context_parts)

    user_prompt = f"""Вопрос пользователя:
{question}

Контекст из документов:
{context}

Ответь кратко и по делу. Если информации не хватает, прямо скажи об этом."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
