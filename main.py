import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold

from config import BOT_TOKEN

dp = Dispatcher()
# Adding custom arguments in Dispatcher
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Подобное решение привдёт к ошибке в случае если full_name будет обёрнуто в <> - скобки,
    Они буду восприняты как html-тэг
    :param message:
    :return:
    """
    await message.answer(
        f"Hello, <b>{html.bold(message.from_user.full_name)}</b>!",
        parse_mode=ParseMode.HTML)


@dp.message(Command("hello1"))
async def cmd_hello(message: Message):
    """Первый вариант решения проблемы выше"""
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("hello2"))
async def cmd_hello(message: Message):
    """
    Более универсальное решение проблемы
    :param message:
    :return:
    """
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )


# @dp.message(F.text)
# async def echo_with_time(message: Message):
#     """
#     Обработка пользовательского ввода
#     :param message:
#     :return:
#     """
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="HTML")


# @dp.message(F.text)
# async def extract_data(message: Message):
#     """
#     userdata parsing by aiogram utils
#     :param message:
#     :return:
#     """
#     data = {
#         "url": "<N/A>",
#         "email": "<N/A>",
#         "code": "<N/A>"
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             # Неправильно
#             # data[item.type] = message.text[item.offset : item.offset+item.length]
#             # Правильно
#             data[item.type] = item.extract_from(message.text)
#     await message.reply(
#         "Вот что я нашёл:\n"
#         f"URL: {html.quote(data['url'])}\n"
#         f"E-mail: {html.quote(data['email'])}\n"
#         f"Пароль: {html.quote(data['code'])}"
#     )


@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: Message, mylist: list[int]):
    mylist.append(7)
    await message.answer("Вы добавили число 7")


@dp.message(Command("show_list"))
async def cmd_show_list(message: Message, mylist: list[int]):
    await message.answer(f"List: {mylist}")


@dp.message(Command("info"))
async def cmd_info(message: Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")


# Echo message
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")


# Если не указать фильтр F.text,
# то хэндлер сработает даже на картинку с подписью /test
@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    await message.answer(
        "Hello, <b>world</b>!",
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\\!",
        parse_mode=ParseMode.MARKDOWN_V2
    )


# Использование команд и аргументов
@dp.message(Command("settimer"))
async def cmd_settimer(
        message: Message,
        command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer <time> <message>"
        )
        return
    await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {text_to_send}"
    )


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # add kwargs
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
