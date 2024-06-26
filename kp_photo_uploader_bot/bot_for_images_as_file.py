from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from icecream import ic
from Aiogram.common.bot_commands_list import kp_uploader
from kp_photo_uploader_bot.check_existing_file import create_dir

from get_credentials import Credentials

TOKEN = Credentials().pavlinbl4_bot
ALLOWED_USER_IDS = {123456789, 987654321, 1237220337, 187597961}

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)


class FSMFillForm(StatesGroup):
    add_file = State()  # Состояние ожидания добавления файла
    add_credit = State()  # Состояние ожидания ввода image credit
    add_caption = State()  # Состояние ожидания выбора image caption


async def set_main_menu(bot: Bot):
    await bot.set_my_commands(commands=kp_uploader)


# handler будет срабатывать на команду /start вне состояний
# и предлагать отправить фото, отправив команду /add_image
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот помогает добавлять фото в архив\n\n'
             'Чтобы перейти к отправке фото - '
             'отправьте команду /add_image'
    )


@dp.message(Command(commands='help'), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот помогает добавлять фото в архив\n\n'
             'Чтобы перейти к отправке фото\n'
             'отправьте команду /add_image'
    )


# handler будет срабатывать на команду "/cancel" в любых состояниях,
@dp.message(Command(commands='cancel'))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы прервали работу\n\n'
             'Чтобы вернуться к загрузке фото -\n '
             'отправьте команду /add_image'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# handler_03 будет срабатывать на команду /add_image
# и переводить бота в состояние ожидания загрузки файла
@dp.message(Command(commands='add_image'), StateFilter(default_state), F.from_user.id.in_(ALLOWED_USER_IDS))
async def process_add_image_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, отправьте снимок боту как файл')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.add_file)


# handler_04 будет срабатывать, если отправлено фото
# и переводить в состояние ожидания ввода автора фото
@dp.message(StateFilter(FSMFillForm.add_file))
async def handle_allowed_user_messages(message: types.Message, state: FSMContext):
    if message.document is None:
        await message.answer(f"Отправьте фото «как файл», чтоб сохранить качество\n"
                             f"снимка")
        await state.set_state(FSMFillForm.add_file)
    else:
        uploaded_file = message.document
        file_id = uploaded_file.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path

        allowed_files_type = {'image/jpeg',
                              'image/png',
                              }

        if uploaded_file.mime_type in allowed_files_type:
            # create dir
            uploaded_images = create_dir("Uploaded_images")

            # save file to hdd
            await bot.download_file(file_path, f"{uploaded_images}/{uploaded_file.file_name}.jpg")

            # send message to sender
            await message.answer(f"Hello, {hbold(message.from_user.full_name)}\n"
                                 f"вы загрузили файл - {uploaded_file.file_name} \n"
                                 f"теперь укажите автора/правообладателя снимка")
            # ic(f'path to uploading image : ../DownloadedFiles/{uploaded_file.file_name}.jpg')

            # Устанавливаем состояние ожидания ввода автора фото
            await state.set_state(FSMFillForm.add_credit)

        else:
            await message.answer(f"Вы отправили недопустимый тип файла\n"
                                 f"я работаю только с фотографиями")
            await state.set_state(FSMFillForm.add_file)


# handler будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода описания
@dp.message(StateFilter(FSMFillForm.add_credit), F.text.len() > 3)
async def process_name_sent(message: Message, state: FSMContext):
    # сохраняем введенное имя в хранилище по ключу "credit"
    await state.update_data(credit=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш описание снимка')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.add_caption)


# handler будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода описания
@dp.message(StateFilter(FSMFillForm.add_caption), F.text.len() > 3)
async def process_name_sent(message: Message, state: FSMContext):
    # сохраняем введенное имя в хранилище по ключу "credit"
    await state.update_data(caption=message.text)
    data = await state.get_data()
    # await message.answer(f'{data["caption"]}')
    await message.answer(text='Спасибо!\n\nВ ближайшее время вам поступит id снимка')
    # Устанавливаем состояние ожидания ввода описания
    # await state.set_state(FSMFillForm.add_caption)
    await state.clear()
    ic(f'{data["caption"]}\n{data["credit"]}')


@dp.message(Command(commands='add_image'), StateFilter(default_state))
async def handle_other_messages(message: types.Message):
    # This function will be called for messages from any other user
    with open('users.txt', 'a') as txt_user_base:
        txt_user_base.write(f'{message.from_user.full_name} - {message.from_user.id}\n')
    await message.answer(f"Извините, {hbold(message.from_user.full_name)}\n"
                         f"это частный бот и вы не включены в"
                         f"список пользователей .")


# handler будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода описания
@dp.message(StateFilter(FSMFillForm.add_credit), F.text.len() < 3)
async def process_name_sent(message: Message, state: FSMContext):
    # сохраняем введенное имя в хранилище по ключу "credit"
    await state.update_data(credit=message.text)
    await message.answer(text='текст не может быть короче 3 букв')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.add_credit)


@dp.message(StateFilter(default_state))
async def handle_other_messages_2(message: types.Message):
    # This function will be called for messages from any other user
    await message.answer(f"{hbold(message.from_user.full_name)}\n"
                         f"для начала работы\n"
                         f"отправьте команду /start\n"
                         f"Чтобы загрузить фото\n"
                         f"отправьте команду /add_image\n")


# start polling
if __name__ == '__main__':
    async def set_main_menu(bot: bot):
        await bot.set_my_commands(commands=kp_uploader)


    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
