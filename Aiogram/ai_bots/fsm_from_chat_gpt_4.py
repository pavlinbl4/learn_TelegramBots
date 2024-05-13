import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = 'YOUR_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class Survey(StatesGroup):
    waiting_for_first_answer = State()
    waiting_for_confirmation = State()
    waiting_for_second_answer = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Answer 1"))
    keyboard.add(KeyboardButton("Answer 2"))
    keyboard.add(KeyboardButton("Answer 3"))
    await message.answer("Choose an answer:", reply_markup=keyboard)
    await Survey.waiting_for_first_answer.set()


@dp.message_handler(state=Survey.waiting_for_first_answer)
async def process_first_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_answer'] = message.text
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Yes"))
    keyboard.add(KeyboardButton("No"))
    keyboard.add(KeyboardButton("Cancel"))
    await message.answer(f"You selected: {message.text}. Is that correct?", reply_markup=keyboard)
    await Survey.waiting_for_confirmation.set()


@dp.message_handler(lambda message: message.text.lower() not in ["yes", "no", "cancel"], state=Survey.waiting_for_confirmation)
async def process_invalid_confirmation(message: types.Message):
    return await message.reply("Please choose Yes, No, or Cancel.")


@dp.message_handler(lambda message: message.text.lower() == "cancel", state=Survey.waiting_for_confirmation)
async def process_cancel(message: types.Message, state: FSMContext):
    await message.answer("Survey canceled.", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda message: message.text.lower() == "no", state=Survey.waiting_for_confirmation)
async def process_no(message: types.Message):
    return await cmd_start(message)


@dp.message_handler(lambda message: message.text.lower() == "yes", state=Survey.waiting_for_confirmation)
async def process_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        first_answer = data['first_answer']
    await message.answer("Please type your next answer:", reply_markup=ReplyKeyboardRemove())
    await Survey.waiting_for_second_answer.set()


@dp.message_handler(state=Survey.waiting_for_second_answer)
async def process_second_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_answer'] = message.text
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Yes"))
    keyboard.add(KeyboardButton("No"))
    keyboard.add(KeyboardButton("Cancel"))
    await message.answer(f"You typed: {message.text}. Is that correct?", reply_markup=keyboard)
    await Survey.waiting_for_confirmation.set()


@dp.message_handler(lambda message: message.text.lower() == "yes", state=Survey.waiting_for_confirmation)
async def process_final_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        first_answer = data['first_answer']
        second_answer = data['second_answer']
    await message.answer("Thank you for completing the survey!", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    run_your_application((first_answer, second_answer))