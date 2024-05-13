"""
В этом примере реализованы следующие функции:

    Запуск бота с помощью команды /start.
    Отображение первого вопроса с вариантами ответов в виде inline-кнопок.
    Обработка ответов на первый вопрос и подтверждение выбора.
    Отображение второго вопроса для текстового ввода.
    Обработка ответов на второй вопрос и подтверждение выбора.
    Передача полученных данных в внешнее приложение Python и отображение результата.
    Обработка повторного ввода и отмены операции.

"""

import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

# в импортах ошибки, думаю от старой версии
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher import FSMContext

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния FSM
class FormStates(StatesGroup):
    question1 = State()
    question2 = State()

# Вопросы и варианты ответов
QUESTIONS = [
    {
        'text': 'Вопрос 1',
        'options': ['Вариант 1', 'Вариант 2', 'Вариант 3']
    },
    {
        'text': 'Вопрос 2',
        'options': None  # Текстовый ответ
    }
]

# Запуск бота
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await FormStates.question1.set()
    keyboard = types.InlineKeyboardMarkup()
    for option in QUESTIONS[0]['options']:
        keyboard.add(types.InlineKeyboardButton(text=option, callback_data=option))
    await message.reply(QUESTIONS[0]['text'], reply_markup=keyboard)

# Обработка ответов на вопрос 1
@dp.callback_query_handler(state=FormStates.question1)
async def process_question1(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(question1=answer)
    await callback.message.edit_reply_markup(reply_markup=None)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='no'))
    keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    await callback.message.reply(f'Вы выбрали: {answer}', reply_markup=keyboard)
    await FormStates.next()

# Обработка ответов на вопрос 2
@dp.message_handler(state=FormStates.question2)
async def process_question2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question2=answer)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='no'))
    keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    await message.reply(f'Вы ответили: {answer}', reply_markup=keyboard)

# Обработка подтверждений и отмены
@dp.callback_query_handler(lambda c: c.data in ['yes', 'no', 'cancel'], state='*')
async def process_confirmation(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        data = await state.get_data()
        # Запуск приложения Python с полученными данными
        app_result = run_python_app(data)
        await callback.message.reply(f'Результат работы приложения: {app_result}')
        await state.finish()
    elif callback.data == 'no':
        current_state = await state.get_state()
        if current_state == FormStates.question1.state:
            keyboard = types.InlineKeyboardMarkup()
            for option in QUESTIONS[0]['options']:
                keyboard.add(types.InlineKeyboardButton(text=option, callback_data=option))
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            await FormStates.question2.set()
            await callback.message.reply(QUESTIONS[1]['text'])
    else:
        await state.finish()
        await callback.message.reply('Операция отменена')

# Функция для имитации работы внешнего приложения
def run_python_app(data):
    question1, question2 = data.values()
    # Здесь может быть код для выполнения каких-либо операций
    return f'Ответы: {question1}, {question2}'

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)