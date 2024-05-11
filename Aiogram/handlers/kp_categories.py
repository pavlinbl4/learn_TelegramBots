from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter

from Aiogram.filters.chat_types import ChatTypeFilter

from Aiogram.keyboards import kp_keyboard
from Aiogram.common.category_dict import category_dict
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger

user_categories_router = Router()


class ShootCreation(StatesGroup):
    select_category = State()
    confirm_category = State()
    write_caption = State()
    confirm_caption = State()


@user_categories_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    logger.info(message.text)

    await message.answer("Hello create a shoot",
                         reply_markup=kp_keyboard.kp_keyboard.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Select category",

                         ))
    await state.set_state(ShootCreation.select_category)


@user_categories_router.message(ShootCreation.select_category, F.text.in_(category_dict))
async def start_cmd(message: types.Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(category=message.text)
    await message.answer(message.text,
                         reply_markup=kp_keyboard.delete_kb)
    await state.set_state(ShootCreation.confirm_category)


@user_categories_router.message(ShootCreation.confirm_category, F.text.in_(category_dict))
async def confirm_cmd(message: types.Message, state: FSMContext):
    await state.update_data(confirm=message.text)
    logger.info(message.text)
    await message.answer("Please confirm",
                         reply_markup=kp_keyboard.confirm_keyboard.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Confirm category",

                         ))
    await message.answer(f"You confirmed category {message.text}",
                         reply_markup=kp_keyboard.delete_kb)
    data = await state.get_data()
    await message.answer(f'you select {data["category"]} - {data["confirm"]}')
