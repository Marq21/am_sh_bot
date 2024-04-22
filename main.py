import json
import sqlite3
import webbrowser

import requests
import telebot
from currency_converter import CurrencyConverter
from telebot import types

converter = CurrencyConverter()
bot = telebot.TeleBot('6974044588:AAHE5FE7oDPob7pJ_49I4sWzhE8K-_5_SOc')

login = ""
password = ""
API_KEY = '7454ddf76d882614c5424f640009a0ff'
amount = 0


@bot.message_handler(commands=['convert'])
def convert_currency(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введит число.')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше нуля. Введит число.')
        bot.register_next_step_handler(message, summa)
        return


@bot.callback_query_handler(func=lambda callback: True)
def callback_data_currency(callback):
    if callback.data != 'else':
        values = callback.data.upper().split('/')
        res = converter.convert(amount, values[0], values[1])
        bot.send_message(callback.message.chat.id,
                         f'Результат: {round(res, 2)}\nВведите следующую сумму для конвертации')
        bot.register_next_step_handler(callback.message, summa)
    else:
        bot.send_message(callback.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(callback.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = converter.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id,
                         f'Результат: {round(res, 2)}\nВведите следующую сумму для конвертации')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id,
                         f'Введите  существующую пару. Попробуйте ещё раз ')
        bot.register_next_step_handler(message, my_currency)


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
    con = sqlite3.connect('sq_db.sql')
    cursor = con.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(100), pass varchar(50))')
    con.commit()
    cursor.close()
    con.close()

    bot.send_message(message.chat.id, 'Login')
    bot.register_next_step_handler(message, user_name)


@bot.message_handler(commands=['temp_forecast'])
def weather_forecast(message):
    bot.send_message(message.chat.id, 'Введите название города')
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    if result.status_code == 200:
        data = json.loads(result.text)
        bot.reply_to(message, f'Погода в городе {city.capitalize()} сейчас: {data['main']['temp']}')
    else:
        bot.reply_to(message, f'Города {city.capitalize()} не существует')


def user_name(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id, 'Password')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    global password
    password = message.text.strip()

    con = sqlite3.connect('sq_db.sql')
    cursor = con.cursor()

    cursor.execute(
        "INSERT INTO users(name, pass) VALUES('%s', '%s')" % (login, password))
    con.commit()
    cursor.close()
    con.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))

    bot.send_message(message.chat.id, 'Success!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def user_list(call):
    con = sqlite3.connect('sq_db.sql')
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM users")
    users = cursor.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'
    con.commit()
    cursor.close()
    con.close()

    bot.send_message(call.message.chat.id, info)


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
                     f'{message.from_user.first_name} {message.from_user.last_name} программист! :]')


@bot.message_handler()
def user_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'<b>Hello</b> {message.from_user.first_name}', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(non_stop=True)
