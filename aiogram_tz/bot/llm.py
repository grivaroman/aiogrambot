import json
import re
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

SYSTEM_PROMPT = """
Ты SQL-генератор для PostgreSQL (psycopg2).

Правила:
- Используй ТОЛЬКО %s как placeholder
- Верни ТОЛЬКО JSON, без текста и без ````
- Формат:

{
  "sql": "SQL запрос",
  "params": []
}

Если запрос невозможно обработать — верни:

{
  "sql": null,
  "params": []
}
"""

def extract_json(text: str) -> str:
    """
    Убирает ```json ``` и всё лишнее
    """
    text = text.strip()

    # убираем ```json и ```
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    return text.strip()

def parse_query(text: str) -> dict:
    try:
        resp = client.chat.completions.create(
            model="google/gemma-2-9b-it",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0,
            max_tokens=256
        )

        raw = resp.choices[0].message.content
        print("LLM RAW:", raw)

        clean = extract_json(raw)
        parsed = json.loads(clean)

        return parsed

    except Exception as e:
        print("LLM error:", e)
        return {"sql": None, "params": []}
