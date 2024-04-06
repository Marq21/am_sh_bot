import webbrowser

import telebot
from telebot import types

bot = telebot.TeleBot('6974044588:AAHE5FE7oDPob7pJ_49I4sWzhE8K-_5_SOc')


@bot.message_handler(content_types=['photo'])
def pdf_handler(message):
    """
    pdf_handling
    :param message:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Поиск', url='https://google.com')
    markup.row(button1)
    button2 = types.InlineKeyboardButton('Удалить', callback_data='delete')
    button3 = types.InlineKeyboardButton('Изменить', callback_data='edit')
    markup.row(button2, button3)
    bot.reply_to(message, 'message', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['site', 'website'])
def site_handler(message):
    """
    browser handling
    :param message:
    :return:
    """
    webbrowser.open('https://vk.com/sruzvelt')


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Поиск')
    markup.row(button1)
    button2 = types.KeyboardButton('Удалить')
    button3 = types.KeyboardButton('Изменить')
    markup.row(button2, button3)
    bot.send_message(message.chat.id, 'You!', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Поиск':
        bot.send_message(message.chat.id, 'Website is open!')
    elif message.text == 'Удалить':
        bot.send_message(message.chat.id, 'Deleting!')
    elif message.text == 'Изменить':
        bot.send_message(message.chat.id, 'Editing!')


@bot.message_handler(commands=['help'])
def main_help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em>message</em>!', parse_mode='html')


@bot.message_handler(commands=['show_message'])
def main_show_message(message):
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name} {message.from_user.last_name} хуёвый программист! :]')


@bot.message_handler()
def user_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'<b>Hello</b> {message.from_user.first_name}', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(non_stop=True)
