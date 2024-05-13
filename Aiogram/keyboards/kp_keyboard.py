from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from Aiogram.common.category_dict import category_dict

kp_keyboard = ReplyKeyboardBuilder()
for key, value in category_dict.items():
    kp_keyboard.button(text=key, callback_data=value, )

kp_keyboard.adjust(4, repeat=False)
kp_keyboard.row(KeyboardButton(text='cancel'))





confirm_keyboard = ReplyKeyboardBuilder().add(
    KeyboardButton(text="YES"),
    KeyboardButton(text="NO")
)


delete_kb = ReplyKeyboardRemove()
