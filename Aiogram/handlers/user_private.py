from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, Command, or_f
from Aiogram.filters.chat_types import ChatTypeFilter
from Aiogram.keyboards import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hello I am virtual servant",
                         reply_markup=reply.start_kb2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Abracadabra"
                         ))


@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'menu')))
async def echo(message: types.Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'answer')
    # await message.answer(message.text)
    await message.answer("It's menu", reply_markup=reply.delete_kb)


@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'about')))
async def start_cmd(message: types.Message):
    await message.answer("About us")


@user_private_router.message(or_f(Command('payment'), (F.text.lower() == 'payment')))
async def start_cmd(message: types.Message):
    await message.answer("How to pay")


@user_private_router.message(or_f(Command('shipping'), (F.text.lower() == 'shipping')))
async def start_cmd(message: types.Message):
    await message.answer("Shipping version")


# @user_private_router.message(F.text)
# async def start_cmd(message: types.Message):
#     await message.answer("Magic filter")
    # print("Magic filter")


@user_private_router.message(F.photo)
async def start_cmd(message: types.Message):
    await message.answer("Magic filter for photo")


@user_private_router.message(F.file)
async def start_cmd(message: types.Message):
    await message.answer("Magic filter for file")
