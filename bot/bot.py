from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import bot_settings
from handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    if not bot_settings.bot_token:
        raise RuntimeError("BOT_TOKEN is empty. Set it in .env")

    bot = Bot(token=bot_settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
