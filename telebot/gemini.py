import telebot
from get_credentials import Credentials

TOKEN = Credentials().crazypythonbot

# Файл с данными о подписчиках
SUBSCRIBERS_FILE = "subscribers.txt"


# Функция для проверки подписки
def is_subscribed(user_id):
    with open(SUBSCRIBERS_FILE, "r") as f:
        subscribers = f.readlines()
    return str(user_id) + "\n" in subscribers


# Функция для подписки пользователя
def subscribe(user_id):
    with open(SUBSCRIBERS_FILE, "a") as f:
        f.write(str(user_id) + "\n")


# Функция для отписки пользователя
def unsubscribe(user_id):
    with open(SUBSCRIBERS_FILE, "r") as f:
        subscribers = f.readlines()
    with open(SUBSCRIBERS_FILE, "w") as f:
        for subscriber in subscribers:
            if subscriber != user_id + "\n":
                f.write(subscriber)


# Токен бота
bot_token = TOKEN

# Создание экземпляра бота
bot = telebot.TeleBot(bot_token)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if is_subscribed(user_id):
        bot.send_message(message.chat.id, "Вы уже подписаны на сообщения.")
    else:
        subscribe(user_id)
        bot.send_message(message.chat.id, "Вы успешно подписались на сообщения!")


# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id

    if is_subscribed(user_id):
        unsubscribe(user_id)
        bot.send_message(message.chat.id, "Вы отписались от сообщений.")
    else:
        bot.send_message(message.chat.id, "Вы не были подписаны на сообщения.")


# Функция для рассылки сообщений
def send_message(message):
    with open(SUBSCRIBERS_FILE, "r") as f:
        subscribers = f.readlines()

    # Рассылка сообщения всем подписчикам
    for subscriber in subscribers:
        bot.send_message(subscriber.strip(), message)


# Запуск бота
bot.polling()
# send_message("слыщмите меня бандерлоги?")
