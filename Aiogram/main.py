from aiogram import Bot, Dispatcher
import asyncio
from aiogram.types import Message
from get_credentials import Credentials

token = Credentials().crazypythonbot


async def start_bot(bot: Bot):
    await bot.send_message(187597961, text="I am working Boss")


async def stop_bot(bot: Bot):
    await bot.send_message(187597961, text="Bot stoped")


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f' Hy ! {message.from_user.first_name}')
    await message.answer(f' Hy ! {message.from_user.first_name}')
    await message.reply(f' Hy ! {message.from_user.first_name}')


async def start():
    bot = Bot(token=token)

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
