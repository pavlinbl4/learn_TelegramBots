import asyncio
import logging
import sys
import types
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from Aiogram.keyboards import kp_keyboard
from get_credentials import Credentials

TOKEN = getenv("BOT_TOKEN")

form_router = Router()


class Form(StatesGroup):
    name = State()
    confirm = State()
    caption = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Для создания съемки\nвыберите категорию",
                         reply_markup=kp_keyboard.kp_keyboard.as_markup(
                             resize_keyboard=True,
                         ))


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "*Оформление съемки отменено*",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.confirm)
    await message.answer(
        f"_Выбрана категория_ \n*{message.text}*\nПодтвердите ваш выбор",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.confirm, F.text.casefold() == "no")
async def process_bad_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Запустите бота заново командой\n**/start**",
        reply_markup=ReplyKeyboardRemove(),
    )
    await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.confirm, F.text.casefold() == "yes")
async def process_good_category(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.caption)
    data = await state.get_data()

    await message.reply(
        f"_Выбрана категория_: *{data['name']}*\nВведите описание съемки",
        reply_markup=ReplyKeyboardRemove(),
    )


# @form_router.message(Form.confirm)
# async def process_unknown_write_bots(message: Message) -> None:
#     await message.reply("I don't understand you :(")


@form_router.message(Form.caption)
async def process_caption(message: Message, state: FSMContext) -> None:
    data = await state.update_data(caption=message.text)
    await state.clear()
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    caption = data.get("caption"
                       )
    text = f"Категория - *{name}*\n"
    text += (
        f"_описание съемки_: *{caption}*"
        if positive
        else "_ошибки бывают у всех_"
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():
    TOKEN = Credentials().pavlinbl4_bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
