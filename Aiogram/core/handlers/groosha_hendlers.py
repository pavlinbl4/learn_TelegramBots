from aiogram import Bot, types
from aiogram.types import Message


# Хэндлер на команду /start
# @dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello from Groosha bot!")

async def cmd_test1(message: types.Message):
    await message.reply("Test 1 Groosha bot!")

# Хэндлер на команду /test2
async def cmd_test2(message: types.Message):
    await message.reply("Test 2 Groosha bot!")
