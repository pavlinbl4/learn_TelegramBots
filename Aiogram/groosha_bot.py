import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from get_credentials import Credentials

from Aiogram.core.handlers.groosha_hendlers import cmd_start, cmd_test1, cmd_test2
from aiogram.types import Message

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Запуск процесса поллинга новых апдейтов
async def main():
    token = Credentials().pavlinbl4_bot
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.message.register(cmd_test2, Command("test2"))
    dp.message.register(cmd_test1, Command("test1"))
    dp.message.register(cmd_start, Command("start"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
