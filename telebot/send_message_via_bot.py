import telebot
from get_credentials import Credentials

TOKEN = Credentials().crazypythonbot

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Список пользователей
users = [5076064265, 187597961, ]  # Здесь перечисляйте chat_id пользователей или их username

def send_message_to_users(message):
    for user in users:
        bot.send_message(user, message)

 # Пример использования
send_message_to_users("Привет! Это информационное сообщение для вас.")


# Запуск бота
bot.polling()



