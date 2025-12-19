from aiogram import Router, types
from llm import parse_query
from db import fetch_value

router = Router()

@router.message()
async def handle_message(message: types.Message):
    """
    1. Получаем текст
    2. Парсим NL → SQL через LLM
    3. Выполняем SQL
    4. Возвращаем одно число
    """

    user_text = message.text.strip()

    try:
        parsed = parse_query(user_text)
    except Exception:
        await message.answer("0")
        return

    sql = parsed.get("sql")
    params = parsed.get("params", [])

    if not sql:
        await message.answer("0")
        return

    try:
        value = fetch_value(sql, tuple(params))
    except Exception:
        await message.answer("0")
        return

    await message.answer(str(value))
