import requests


questions = [
    "Что такое персональные данные?",
    "Какие обязанности есть у оператора персональных данных?",
    "Что такое коммерческая тайна?",
    "Какие требования предъявляются к возврату товара?",
]


for question in questions:
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question},
        timeout=60,
    )
    print("=" * 80)
    print("QUESTION:", question)
    print(response.json())
