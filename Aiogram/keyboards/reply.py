from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='menu'),
         KeyboardButton(text='about'),

         ],
        [KeyboardButton(text='payment')]
    ], resize_keyboard=True,
    input_field_placeholder="What are you want?"
)

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='menu'),
    KeyboardButton(text='about'),
    KeyboardButton(text='payment'),
    KeyboardButton(text='shipping')
)
start_kb2.adjust(2, 1, 1)

delete_kb = ReplyKeyboardRemove()

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text='new button'))
# start_kb3.add(KeyboardButton(text='new button'))
# start_kb3.adjust(1, 1, 1, 1)


