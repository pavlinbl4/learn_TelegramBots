import asyncio
from aiogram import Bot, Dispatcher, types

from Aiogram.handlers.kp_categories import user_categories_router
from get_credentials import Credentials
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
# from common.bot_commands_list import private

token = Credentials().pavlinbl4_bot

bot = Bot(token)
bot.my_admins_list = []

dp = Dispatcher()

dp.include_routers(user_private_router)
dp.include_routers(user_group_router)


ALLOWED_UPDATES = ['message', 'edited message']


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
