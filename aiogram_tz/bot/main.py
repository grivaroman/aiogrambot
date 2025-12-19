import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from db import fetch_value
from llm import parse_query


bot = Bot(token="7803028383:AAGwg2xXgVNPpV8i26iGczDLUmHUK9fJ1JU")
dp = Dispatcher()


@dp.message()
async def handle(message: Message):
    try:
        parsed = parse_query(message.text)

        # лог для отладки (ОЧЕНЬ полезен)
        print("LLM PARSED:", parsed)

        sql = parsed.get("sql")
        params = parsed.get("params", [])

        if not sql:
            await message.answer("Не понял запрос")
            return

        value = fetch_value(sql, tuple(params))
        await message.answer(str(value))

    except Exception as e:
        print("ERROR:", e)
        await message.answer("Ошибка обработки запроса")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
