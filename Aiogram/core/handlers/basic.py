from aiogram import Bot
from aiogram.types import Message


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,
                           f'*** Hy ! {message.from_user.first_name} {message.from_user.last_name}***')
    await message.answer(f'you id :__{message.from_user.id}__')
    await message.answer(f'you username :__{message.from_user.username}__')
    # await message.reply(f' Hy ! {message.from_user.first_name}')


async def get_photo(message: Message, bot: Bot):
    await message.answer("Thank you for picture")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'image.jpg')
