from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from Aiogram.core.handlers.basic import get_start, get_photo
from Aiogram.core.settings import settings
from aiogram.filters import Command
import Aiogram.core.keyboards.keyboard_1 as kb


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="__I am working Boss__",
                           reply_markup=kb.settings)


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Bot stopped")


async def start():
    bot = Bot(token=settings.bots.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_photo, F.content_type == ContentType.PHOTO)
    dp.message.register(get_start, Command(commands=['start', 'run']))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
