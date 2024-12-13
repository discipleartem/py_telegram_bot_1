import telebot
from telebot import types
import configparser

config = configparser.ConfigParser()
config.read('.config')
""".config file
[Config]
KEY = token_without_quoters 
"""
config_key = config.get('Config','KEY')



bot = telebot.TeleBot(config_key)

@bot.message_handler(commands=['start'])
def start(message):
    button = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text='тестовая кнопка 1', callback_data='hello')
    btn2 = types.InlineKeyboardButton(text='Удалить', callback_data='delete')
    btn3 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit')

    button.row(btn1)
    button.row(btn2, btn3)

    bot.send_message(message.chat.id, 'Привет, я тест-бот_1', reply_markup=button)


@bot.message_handler(commands=['help'])
def help_func(message):
    bot.send_message(message.chat.id, 'Help info')

@bot.message_handler(commands=['delete'])
def delete(message):
    bot.delete_message(message.chat.id, message.message_id - 1)


# должен быть в конце
@bot.message_handler(content_types=['text'])
def text_func(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, как дела?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Это фото')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'hello':
        bot.send_message(callback.message.chat.id, 'Hello 1')
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'удалено последнее сообщение')
    elif callback.data == 'edit':
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id +1, #+1 последнее сообщение
                              text='отредактированный текст')
    else:
        bot.send_message(callback.message.chat.id, 'Я не знаю что ответить')








bot.polling(none_stop=True)