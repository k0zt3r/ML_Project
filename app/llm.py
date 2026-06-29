from openai import OpenAI, OpenAIError

from app.config import (
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENROUTER_API_KEY,
)


def get_api_key() -> str | None:
    """Берет ключ OpenRouter или OpenAI из переменных окружения."""
    return OPENROUTER_API_KEY or OPENAI_API_KEY


def call_openai_compatible(messages: list[dict]) -> str:
    """Вызывает OpenAI-compatible LLM."""
    api_key = get_api_key()

    if not api_key:
        return (
            "LLM API ключ не задан. Укажите OPENROUTER_API_KEY или OPENAI_API_KEY "
            "в переменных окружения."
        )

    try:
        client = OpenAI(api_key=api_key, base_url=LLM_BASE_URL)
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=700,
        )

        answer = response.choices[0].message.content
        return answer.strip()
    except OpenAIError as error:
        return (
            "Ошибка при обращении к LLM. "
            "Проверьте OPENROUTER_API_KEY, LLM_MODEL и доступность выбранной модели. "
            f"Техническая ошибка: {error}"
        )


def call_llm(messages: list[dict]) -> str:
    """Вызывает выбранного LLM-провайдера."""
    return call_openai_compatible(messages)
