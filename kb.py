from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from parser import get_category_text


async def get_keyboard_text(url: str):
    list_of_categories = get_category_text(url)
    category_kb_builder = ReplyKeyboardBuilder()
    for category in list_of_categories:
        category_kb_builder.add(KeyboardButton(text=category))
    return category_kb_builder.adjust(1).as_markup()
