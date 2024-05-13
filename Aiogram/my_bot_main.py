import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from Aiogram.handlers.kp_categories import user_categories_router
from Aiogram.handlers.kp_fsm import form_router
from get_credentials import Credentials


import logging

logging.basicConfig(level=logging.INFO)

token = Credentials().pavlinbl4_bot

bot = Bot(token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
# dp.include_routers(user_categories_router)
dp.include_routers(form_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
