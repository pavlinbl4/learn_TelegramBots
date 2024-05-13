from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

from get_credentials import Credentials
from aiogram.utils.markdown import hbold
from icecream import ic

# Configuration
TOKEN = Credentials().pavlinbl4_bot
ALLOWED_USER_IDS = {123456789, 987654321, 1237220337, 187597961}

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher(storage=storage)

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# создаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_file = State()  # Состояние ожидания добавления файла
    add_credit = State()  # Состояние ожидания ввода image credit
    add_caption = State()  # Состояние ожидания выбора image caption


# handler будет срабатывать на команду /start вне состояний
# и предлагать отправить фото, отправив команду /add_image
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот помогает добавлять фото в архив\n\n'
             'Чтобы перейти к отправке фото - '
             'отправьте команду /add_image'
    )


# handler будет срабатывать на команду "/cancel" в любых состояниях,
@dp.message(Command(commands='cancel'))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы прервали работу\n\n'
             'Чтобы вернуться к загрузке фото - '
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
        # ic(uploaded_file)

        # get file path
        file = await bot.get_file(file_id)
        file_path = file.file_path

        allowed_files_type = {'image/jpeg',
                              'image/png',
                              }

        if uploaded_file.mime_type in allowed_files_type:

            # save file to hdd
            await bot.download_file(file_path, f"DownloadedFiles/{uploaded_file.file_name}.jpg")

            # send message to sender
            await message.answer(f"Hello, {hbold(message.from_user.full_name)}\n"
                                 f"вы загрузили файл - {uploaded_file.file_name} "
                                 f"теперь укажите автора/правообладателя снимка")
            ic(f'path to uploading image : ../DownloadedFiles/{uploaded_file.file_name}.jpg')

            # Устанавливаем состояние ожидания ввода автора фото
            await state.set_state(FSMFillForm.add_credit)

        else:
            await message.answer(f"Вы отправили недопустимый тип файла - {uploaded_file.mime_type}\n"
                                 f"я работаю только с фотографиями")
            await state.set_state(FSMFillForm.add_file)




# handler будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода описания
@dp.message(StateFilter(FSMFillForm.add_credit))
async def process_name_sent(message: Message, state: FSMContext):
    # сохраняем введенное имя в хранилище по ключу "credit"
    await state.update_data(credit=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш описание снимка')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.add_caption)


# handler будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.add_credit))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# handler будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


@dp.message()
async def handle_other_messages(message: types.Message):
    # This function will be called for messages from any other user
    await message.reply("Sorry, you are not an allowed user.")


# start polling
if __name__ == '__main__':
    dp.run_polling(bot)
