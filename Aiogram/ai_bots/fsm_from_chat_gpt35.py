import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'YOUR_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class SurveyStates(StatesGroup):
    question = State()
    confirmation = State()


@dp.message_handler(commands=['start'])
async def start_survey(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Answer 1"))
    keyboard.add(KeyboardButton("Answer 2"))
    keyboard.add(KeyboardButton("Answer 3"))

    await SurveyStates.question.set()
    await message.answer("Choose an answer:", reply_markup=keyboard)


@dp.message_handler(state=SurveyStates.question)
async def process_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer=answer)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Yes"))
    keyboard.add(KeyboardButton("No"))
    keyboard.add(KeyboardButton("Cancel"))

    await SurveyStates.confirmation.set()
    await message.answer(f"You selected: {answer}. Is that correct?", reply_markup=keyboard)


@dp.message_handler(state=SurveyStates.confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    choice = message.text
    data = await state.get_data()
    answer = data.get('answer')

    if choice.lower() == 'yes':
        # Save answer or process it as needed
        await message.answer(f"Answer '{answer}' saved.")

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Yes"))
        keyboard.add(KeyboardButton("No"))
        keyboard.add(KeyboardButton("Cancel"))

        await message.answer("Do you want to continue?", reply_markup=keyboard)
    elif choice.lower() == 'no':
        await message.answer("Choose an answer again:", reply_markup=ReplyKeyboardRemove())
        await SurveyStates.question.set()
    elif choice.lower() == 'cancel':
        await message.answer("Survey canceled.", reply_markup=ReplyKeyboardRemove())
        await state.finish()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
