from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from typing import Any, Dict
from aiogram.enums import ParseMode

form_router = Router()


class Form(StatesGroup):
    category = State()
    confirm = State()
    caption = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.category)
    await message.answer(
        "Hi! Write category",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.category)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.confirm)
    await message.answer(
        f"Are you sure, {message.text}!\n",
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


@form_router.message(Form.confirm, F.text.casefold() == "yes")
async def selected_category_good(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.caption)
    data = await state.get_data()

    await message.reply(
        f"Selected category '{data['name']}'\nNow write caption",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.confirm, F.text.casefold() == "no")
async def selected_category_bad(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Not bad not terrible.\nSee you soon.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await show_summary(message=message, data=data, positive=False)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    category_name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {category_name}, "
    text += (
        f"you like to write bots with {language}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
