from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/start')],
    [KeyboardButton(text='Busket'), KeyboardButton(text='Contacts')],

], resize_keyboard=True, input_field_placeholder="Press any button")

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Inline',
                   url='https://www.notion.so/'
                       '3efc806bb02242bfbb8cf79ebac60d77?pvs=4#7a9b18e5b235423588a02e098489f83d')]
])
