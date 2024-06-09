import time

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from parser import parse
from utils import handle_json, format_news_category

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(
        """Чтобы начать введите команду /find\nЧтобы проверить последнюю актуальную выдачу введите команду /check""")
    await msg.delete()


@router.message(Command('check'))
async def get_user_url(msg: Message):
    data = await handle_json("items.json")
    for category in data:
        await msg.answer(f'<b>{category}</b>:\n\n{format_news_category(data[category])}')


@router.message(Command('parse'))
async def parse_data(msg: Message):
    await msg.answer("Start parsing")
    start = time.time()
    await parse()
    await msg.answer("Stop parsing")
    print(time.time() - start)
