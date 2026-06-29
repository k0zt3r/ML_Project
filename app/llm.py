from openai import OpenAI

from app.config import LLM_BASE_URL, LLM_MODEL, OPENAI_API_KEY, OPENROUTER_API_KEY


def get_api_key() -> str | None:
    """Берет ключ OpenRouter или OpenAI из переменных окружения."""
    return OPENROUTER_API_KEY or OPENAI_API_KEY


def call_llm(messages: list[dict]) -> str:
    """Вызывает OpenAI-compatible LLM."""
    api_key = get_api_key()

    if not api_key:
        return (
            "LLM API ключ не задан. Укажите OPENROUTER_API_KEY или OPENAI_API_KEY "
            "в переменных окружения."
        )

    client = OpenAI(api_key=api_key, base_url=LLM_BASE_URL)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=700,
    )

    answer = response.choices[0].message.content
    return answer.strip()
